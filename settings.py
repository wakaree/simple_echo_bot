from pathlib import Path
from typing import Union

from pydantic import BaseModel, StrictStr
from yaml import safe_load


class Settings(BaseModel):
    DEFAULT_PATH: str = "config.yml"
    API_TOKEN: StrictStr

    def __init__(self, path: Union[Path, str] = DEFAULT_PATH) -> None:
        with open(path, encoding="utf-8") as file:
            data = safe_load(file)
            super().__init__(**data)
