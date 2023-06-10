from pathlib import Path
from typing import Dict, Any, Tuple, Callable

from pydantic import SecretStr, BaseSettings
from yaml import full_load


def _get_source(settings: BaseSettings) -> Dict[str, Any]:
    config = settings.__config__
    path = Path(config.env_file)

    with path.open(encoding=config.env_file_encoding) as stream:
        return full_load(stream)


class Settings(BaseSettings):
    API_TOKEN: SecretStr

    class Config:
        env_file = "config.yml"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(cls, **_: Any) -> Tuple[Callable[[BaseSettings], Dict[str, Any]]]:
            return _get_source,
