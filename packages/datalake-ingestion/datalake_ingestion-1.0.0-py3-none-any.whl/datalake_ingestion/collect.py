from importlib import import_module
import inspect
import json
import re
from time import perf_counter
from logging import getLogger
from datalake.interface import IStorageEvent
import datalake_ingestion.exceptions
import datalake_ingestion.preprocess
from datalake.telemetry import Measurement
import pendulum
from pkg_resources import resource_stream
from jsonschema import Draft7Validator
import pendulum


STATUS_SUCCESS = "Success"
STATUS_UNKNOWN = "Unknown"
STATUS_ERROR = "Failure"
STATUS_INFECTED = "Infected"


class Collector(IStorageEvent):
    def __init__(self, datalake, collect_config):
        self._logger = getLogger(f"{__name__}.{__class__.__name__}")
        self._datalake = datalake
        self._monitor = datalake.monitor

        with resource_stream("datalake_ingestion", "schemas/collect.json") as f:
            config_schema = json.load(f)
        Draft7Validator.check_schema(config_schema)
        Draft7Validator(config_schema).validate(collect_config)

        builtin_classes = {}
        for n, c in inspect.getmembers(datalake_ingestion.preprocess, inspect.isclass):
            if not issubclass(c, datalake_ingestion.preprocess.Preprocessor):
                continue
            if inspect.isabstract(c):
                continue
            builtin_classes[n.lower()] = c(self._datalake)

        extended_classes = {}
        self._indexed = {}
        self._unindexed = []
        for item in collect_config:
            cfg = {**item}
            cfg["pattern"] = re.compile(item["pattern"])

            action_name = cfg["action_name"]
            if action_name.lower() in builtin_classes:
                cfg["action_class"] = builtin_classes[action_name.lower()]
            elif action_name.lower() in extended_classes:
                cfg["action_class"] = extended_classes[action_name.lower()]
            else:
                # try to find the class and add it to extended_classes
                action_split = action_name.split(".")
                if len(action_split) > 1:
                    class_name = action_split[-1]
                    module_name = ".".join(action_split[:-1])
                    try:
                        module = import_module(module_name)
                    except ModuleNotFoundError:
                        raise ModuleNotFoundError(f"Preprocessor module '{module_name}' cannot be found")

                    action_class = None
                    for n, c in inspect.getmembers(module, inspect.isclass):
                        if n == class_name:
                            action_class = c
                            break
                    if action_class is None:
                        raise AttributeError(f"Preprocessor class '{class_name}' cannot be found in module {module_name}")
                    if not issubclass(c, datalake_ingestion.preprocess.Preprocessor):
                        raise ValueError(f"Preprocessor '{action_name}' cannot be found in module {module_name}")
                    extended_classes[action_name.lower()] = c(self._datalake)
                    cfg["action_class"] = extended_classes[action_name.lower()]
                else:
                    raise ValueError(f"Preprocessor '{action_name}' cannot be found")

            if "action_params" not in cfg:
                cfg["action_params"] = {}

            if "landing_folder" in cfg:
                idx = cfg["landing_folder"]
                if idx not in self._indexed:
                    self._indexed[idx] = []
                self._indexed[idx].append(cfg)
            else:
                self._unindexed.append(cfg)

    def process(self, storage, path):
        result = self.identify(path)
        process_metric = Measurement("collector")
        process_metric.add_labels({"source_bucket": storage.name, "source_path": path})
        process_metric.add_measure("file_size", storage.size(path))
        if result is None:  # Path is not recognized from the configuration
            purgatory, target, _ = self._datalake.resolve_path("purgatory", path)
            storage.move(path, target, purgatory)
            process_metric.add_label("status", STATUS_UNKNOWN)
        else:  # Collect configuration available
            if "catalog_entry" in result:
                catalog_entry = self._datalake.get_entry(result["catalog_entry"])
                process_metric.add_labels(
                    {
                        "catalog_entry": catalog_entry["_key"],
                        "catalog_domain": catalog_entry["domain"],
                        "catalog_provider": catalog_entry["provider"],
                        "catalog_feed": catalog_entry["feed"],
                    }
                )
            else:
                catalog_entry = None

            if result["archive"]:
                archive_timestamp = pendulum.now("UTC").format("YYYYMMDD_HHmmSS")
                archive, archive_path, _ = self._datalake.resolve_path("archive", f"{path}.{archive_timestamp}")
                storage.copy(path, archive_path, archive)
                process_metric.add_label("archived", "yes")
                process_metric.add_label("archive_path", archive_path)
            else:
                process_metric.add_label("archived", "no")

            try:
                preprocessor = result["action_class"]
                process_metric.add_label("preprocessor", preprocessor.__class__.__name__)
                preprocessor.action(
                    process_metric,
                    storage,
                    path,
                    result["pattern_extract"],
                    catalog_entry,
                    **result["action_params"],
                )
                process_metric.add_label("status", STATUS_SUCCESS)
            except datalake_ingestion.exceptions.HackDetected as e:
                self._logger.warning(f"Suspicious file {path}: {e} detected")
                quarantine, resolved, _ = self._datalake.resolve_path("quarantine", path)
                storage.move(path, resolved, quarantine)
                process_metric.add_label("status", STATUS_INFECTED)
            except datalake_ingestion.exceptions.PreprocessError as e:
                self._logger.error(f"'{preprocessor.__class__.__name__}' Preprocessor failed file {path}: {e}")
                purgatory, resolved, _ = self._datalake.resolve_path("purgatory", path)
                storage.move(path, resolved, purgatory)
                process_metric.add_label("status", STATUS_ERROR)
            except Exception as e:
                self._logger.error(f"An error occured whilst preprocessing {path}: {str(e)}")
                purgatory, resolved, _ = self._datalake.resolve_path("purgatory", path)
                storage.move(path, resolved, purgatory)
                process_metric.add_label("status", STATUS_ERROR)

        process_metric.add_measure("processing_time", round(process_metric.read_chrono() // 10 ** 6))

        self._monitor.push(process_metric)

    def identify(self, path):
        config = self._unindexed
        for idx in self._indexed.keys():
            if idx in path:
                config = self._indexed[idx]

        for item in config:
            match = item["pattern"].search(path)
            if match is not None:
                result = {**item}
                if "pattern_extract" in result:
                    for var, template in result["pattern_extract"].items():
                        result["pattern_extract"][var] = template.format(capture=match.groups())
                else:
                    result["pattern_extract"] = {}
                return result
        return None
