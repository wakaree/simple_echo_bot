from pydantic import SecretStr

from utils.yaml_reader import YAMLSettings, YAMLSettingsConfig


class Settings(YAMLSettings):
    API_TOKEN: SecretStr

    model_config = YAMLSettingsConfig(env_file_encoding="utf-8", yaml_file=("config.yml",))
