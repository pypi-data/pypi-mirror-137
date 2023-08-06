from abc import ABC, abstractmethod
import csv
from logging import getLogger
import os
from shutil import rmtree, copyfileobj
from tempfile import mkdtemp, mkstemp
import gzip, lzma
import tarfile, zipfile
from datalake_ingestion.exceptions import PreprocessFailed, HackDetected


class Preprocessor(ABC):  # pragma: no cover
    def __init__(self, datalake):
        self._datalake = datalake
        self._logger = getLogger(f"{__name__}.{__class__.__name__}")

    @property
    def logger(self):
        return self._logger

    @abstractmethod
    def action(self, metric, storage, path, path_extracts, catalog_entry, **kwargs):
        """
        Main method is called by the Collector
        """
        raise NotImplementedError()


class LocalPreprocessor(Preprocessor):
    """
    Abstract preprocessor for dealing with local files
    Useful when a file needs to be downloaded for processing
    """

    def new_temp_dir(self, prefix=""):
        return mkdtemp(prefix=f"datalake-preprocess_{prefix}_")

    def new_temp_file(self, prefix="", suffix=".dat"):
        (temp_file, temp_path) = mkstemp(prefix=f"datalake-preprocess_{prefix}_", suffix=suffix)
        os.close(temp_file)
        return temp_path


class Ignore(Preprocessor):
    """
    Either delete or move to a trash storage
    """

    def action(self, metric, storage, path, path_extracts, catalog_entry, immediately=False):
        if immediately:
            storage.delete(path)
        else:
            trash, target, _ = self._datalake.resolve_path("trash", path)
            storage.move(path, target, trash)
            metric.add_labels({"target_store": "trash", "target_path": target})


class Transfer(Preprocessor):
    """
    Move a file to another storage location as-is
    """

    def action(self, metric, storage, path, path_extracts, catalog_entry, destination, new_path=None):
        new_path = new_path.format(**path_extracts) if new_path is not None else path
        dest, target, _ = self._datalake.resolve_path(destination, new_path)
        storage.move(path, target, dest)
        metric.add_labels({"target_store": destination, "target_path": target})


class Extract(LocalPreprocessor):
    """
    Extracts files from an archive or decompresses a file
    """

    def action(self, metric, storage, path, path_extracts, catalog_entry, destination, folder=""):
        arc_file = self.new_temp_file("extract", ".arc")
        tmp_dir = self.new_temp_dir("extract")
        try:
            storage.download(path, arc_file)
            extracted_files = []
            if zipfile.is_zipfile(arc_file):
                metric.add_label("extract_method", "zip")
                with zipfile.ZipFile(arc_file) as f:
                    extracted_files = f.namelist()
                    Extract.check_zip_slip(extracted_files)
                    f.extractall(tmp_dir)
            elif tarfile.is_tarfile(arc_file):
                metric.add_label("extract_method", "tar")
                with tarfile.open(arc_file, "r:*") as f:
                    extracted_files = f.getnames()
                    Extract.check_zip_slip(extracted_files)
                    f.extractall(tmp_dir)
            else:  # Try single file compression
                decompressed_path, _ = os.path.splitext(os.path.basename(path))
                output = os.path.join(tmp_dir, decompressed_path)
                extracted_files = [decompressed_path]
                with open(arc_file, "rb") as f:
                    # Read the file header and guess from the magic number
                    magic = f.read(8)

                # [GZIP file](http://www.zlib.org/rfc-gzip.html#header-trailer)
                if magic[:2] == b"\x1F\x8B":
                    metric.add_label("extract_method", "gzip")
                    with gzip.open(arc_file, "rb") as f_in:
                        with open(output, "wb") as f_out:
                            copyfileobj(f_in, f_out)
                # [XZ file](https://tukaani.org/xz/xz-file-format.txt)
                elif magic[:6] == b"\xFD\x37\x7A\x58\x5A\x00":
                    metric.add_label("extract_method", "lzma")
                    with lzma.open(arc_file, "rb") as f_in:
                        with open(output, "wb") as f_out:
                            copyfileobj(f_in, f_out)
                else:
                    raise PreprocessFailed(f"Compression not found in file {path}")

            metric.add_measure("extracted_files", len(extracted_files))
            metric.add_labels({"target_store": destination, "target_path": folder})

            for extracted_file in extracted_files:
                src_path = os.path.join(tmp_dir, extracted_file)
                dest_path = os.path.join(folder, extracted_file)
                dest, target, _ = self._datalake.resolve_path(destination, dest_path)

                self._datalake.get_storage(dest).upload(src_path, target)
            storage.delete(path)
        except HackDetected as e:
            metric.add_label("vulnerability", e.message)
            raise
        finally:
            rmtree(tmp_dir)
            os.remove(arc_file)

    def check_zip_slip(members):
        """
        Detect directory traversal in archive file
        """
        for member in members:
            if member.startswith("/") or member.startswith("../") or member.startswith("..\\"):
                raise HackDetected("Zip Slip")


class StandardizeCSV(LocalPreprocessor):
    """
    Transforms a csv file in the datalake's standard csv format
    """

    def action(
        self,
        metric,
        storage,
        path,
        path_extracts,
        catalog_entry,
        destination="raw",
        encoding="utf-8",
        headers=0,
        delimiter=",",
        newline="\n",
        escape=None,
        quote='"',
        lang="en_US",
        date_formats=None,
    ):
        format_in = {
            "delimiter": delimiter,
            "lineterminator": newline,
            "escapechar": escape,
            "quoting": csv.QUOTE_MINIMAL if quote is not None else csv.QUOTE_NONE,
            "quotechar": quote,
        }

        file_in = self.new_temp_file("standardize-csv", ".in.csv")
        file_out = self.new_temp_file("standardize-csv", ".out.csv")
        try:
            storage.download(path, file_in)
            reader = csv.reader(self.line_iterator(file_in, encoding, newline, **path_extracts), **format_in)
            with self._datalake.new_dataset_builder(catalog_entry["_key"], file_out, lang, date_formats) as dsb:
                row_count = 0
                try:
                    for row in reader:
                        row_count += 1
                        if row_count <= headers:
                            # skip headers
                            continue
                        dsb.add_sequence(row)

                except Exception as error:
                    msg = f"CSV Parsing failed on line {row_count + 1}: {error}"
                    metric.add_label("error_message", msg)
                    raise PreprocessFailed(msg)

            metric.add_measure("row_count", row_count - headers)
            target_path = self._datalake.upload(
                file_out,
                destination,
                catalog_entry["_key"],
                path_extracts,
                content_type="text/csv",
                encoding="utf-8",
                metadata={**path_extracts},
            )
            metric.add_labels({"target_store": destination, "target_path": target_path})
            storage.delete(path)
        finally:
            os.remove(file_out)
            os.remove(file_in)

    def line_iterator(self, file_in, encoding, newline, **path_extracts):
        """
        Return an itertor for each lines in the file.
        May be overriden in subclass to add specific lines transformations
        (!) but the line itself must not be CSV parsed
        """
        with open(file_in, mode="r", encoding=encoding, newline=newline) as f:
            for line in f.readlines():
                yield line.replace(newline, "")
