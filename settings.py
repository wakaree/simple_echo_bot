
from pydantic import SecretStr

from utils import YAMLSettings


class Settings(YAMLSettings):
    API_TOKEN: SecretStr

    class Config:
        yaml_file = "config.yml",
        env_file_encoding = "utf-8"
