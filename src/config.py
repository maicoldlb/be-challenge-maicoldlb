import os
import json
from typing import NamedTuple, Any

from singleton_decorator import singleton

APP_ENV = os.environ.get("APP_ENV", "dev")


FootballAPI = NamedTuple("FootballAPI", [("url", str), ("token", str)])


@singleton
class Config:
    def __init__(
        self,
        environment: str = os.environ.get("APP_ENV", "dev"),
    ):
        self.environment = environment
        self.config_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "./setting/{env}.json".format(env=environment.lower()))
        )

        self.__config = self.read_config(path=self.config_file_path)

    def read_config(self, path: str) -> Any:
        with open(path, "r+", encoding="utf-8") as f:
            config = json.load(f)
            return config

    @property
    def football_api(self) -> FootballAPI:
        football = self.__config["api"]["football"]
        return FootballAPI(url=football["url"], token=football["token"])


config = Config(environment=APP_ENV)
