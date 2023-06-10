from os import PathLike
from pathlib import Path
from typing import Dict, Any, Tuple, Callable, cast, Union

from pydantic import SecretStr, BaseSettings
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
        def customise_sources(cls, **_: Any) -> Tuple[Callable[[BaseSettings], Dict[str, Any]]]:
            return _get_source,
