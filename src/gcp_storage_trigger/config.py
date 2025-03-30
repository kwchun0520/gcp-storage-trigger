from pydantic import Field
from pydantic_settings import BaseSettings
from loguru import logger
import yaml
from typing import List


CONFIG_PATH = "./config/config.yaml"

class AppSettings(BaseSettings):
    tables:List[str] = Field(List[str], title="List of tables to process")
    delta_suffix:str = Field(str, title="Suffix for the delta table")


def get_config() -> AppSettings:
    with open(CONFIG_PATH, 'r') as stream:
        config_specs = yaml.safe_load(stream)
        config = AppSettings(**config_specs)
    logger.debug(config)
    return config


CONFIG = get_config()
