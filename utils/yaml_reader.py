
from os import PathLike
from pathlib import Path
from typing import cast, Any, Dict, Tuple, Union

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from yaml import full_load


def _get_source(settings: BaseSettings) -> Dict[str, Any]:
    config = cast(YAMLSettings.Config, settings.__config__)
    data: Dict[str, Any] = {}

    for path in config.yaml_file:
        with open(path, encoding=config.env_file_encoding) as stream:
            data.update(
                cast(Dict[str, Any], full_load(stream))
            )

    return data


class YAMLSettings(BaseSettings):
    class Config:
        yaml_file: Tuple[Union[str, PathLike[str], Path], ...] = ()
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls, **_: SettingsSourceCallable
        ) -> Tuple[SettingsSourceCallable, ...]:
            return _get_source,
