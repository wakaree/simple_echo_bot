from os import PathLike
from pathlib import Path
from typing import cast, Any, Dict, Tuple, Union

from pydantic import BaseSettings, SecretStr
from pydantic.env_settings import SettingsSourceCallable
from yaml import full_load


def _get_source(settings: BaseSettings) -> Dict[str, Any]:
    path = Path(
        cast(
            Union[str, PathLike[str]],
            settings.__config__.env_file
        )
    )

    with path.open(
        encoding=settings.__config__.env_file_encoding
    ) as stream:
        return cast(Dict[str, Any], full_load(stream))


class Settings(BaseSettings):
    API_TOKEN: SecretStr

    class Config:
        env_file = "config.yml"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(cls, **_: Any) -> Tuple[SettingsSourceCallable, ...]:
            return _get_source,
