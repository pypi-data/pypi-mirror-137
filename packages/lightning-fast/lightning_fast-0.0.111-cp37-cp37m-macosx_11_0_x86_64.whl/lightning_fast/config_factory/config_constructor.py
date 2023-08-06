import logging
import os
from typing import TypeVar, Generic

import yaml

T = TypeVar("T")


class Config(Generic[T]):
    """
    using BASE_DIR = pathlib.Path(__file__).absolute().parent define your base path
    using
    class DirectoryCollection(dict):
        base_dir = DirectoryDescriptor(BASE_DIR)
        data_dir = DirectoryDescriptor(DATA_DIR)
        log_dir = DirectoryDescriptor(LOG_DIR)
        tmp_dir = DirectoryDescriptor(TMP_DIR)
    define your directory collection
    """

    def __init__(self, config_path, directories: T):
        self.config_path = config_path
        self.directories: T = directories
        self.environment = None
        self.important_static_config = None
        self.mongodbs = None
        self.redis = None
        self.external_api = None
        self.common_static_config = None
        self.kafka_producer = None
        self._get_env()
        self._get_config()
        self._set_log_level()

    def _get_env(self):
        if (
            not os.environ.get("CODE_ENV")
            or os.environ.get("CODE_ENV") == "development"
        ):
            self.environment = "development"
        elif os.environ.get("CODE_ENV") == "staging":
            self.environment = "staging"
        elif os.environ.get("CODE_ENV") == "production":
            self.environment = "production"
        else:
            raise ValueError("Env Wrong!")
        print(f"Current 'CODE_ENV' is '{self.environment}'")

    def _set_log_level(self):
        if self.environment == "production":
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.DEBUG)

    def _get_config(self):

        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                static_config = yaml.safe_load(f)
                if static_config is None:
                    self.important_static_config = None
                else:
                    if self.environment == "development":
                        self.important_static_config = static_config.get("development")
                    elif self.environment == "staging":
                        self.important_static_config = static_config.get("staging")
                    elif self.environment == "production":
                        self.important_static_config = static_config.get("production")
                    else:
                        raise ValueError("Env Wrong!")
                    if not self.important_static_config:
                        logging.warning(
                            "Not have import static config (development or production)"
                        )
                    else:
                        if "mongodbs" not in self.important_static_config:
                            logging.warning("Not have 'mongodbs' in settings.yaml")
                            self.mongodbs = None
                        else:
                            self.mongodbs = self.important_static_config["mongodbs"]
                        if "redis" not in self.important_static_config:
                            logging.warning("Not have 'redis' in settings.yaml")
                            self.redis = None
                        else:
                            self.redis = self.important_static_config["redis"]
                        if "external_api" not in self.important_static_config:
                            logging.warning("Not have 'external_api' in settings.yaml")
                            self.external_api = None
                        else:
                            self.external_api = self.important_static_config[
                                "external_api"
                            ]
                self.common_static_config = static_config.get("common")
