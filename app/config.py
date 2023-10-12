"""
core configuration for api
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    class to represent the core settings for the api
    """
    # batch env variables
    PROJECT_NAME: str = Field(env="PROJECT_NAME")
    VERSION: str = "1.0.0"
    ENV: Optional[str] = Field(env='ENV') if Field(env='ENV') is not None else "develop"
    # database env variables
    MONGO_SERVER: str = Field(env="MONGO_SERVER")
    MONGO_USER: str = Field(env="MONGO_USER")
    MONGO_PASS: str = Field(env="MONGO_PASS")
    MONGO_DB: str = Field(env="MONGO_DB")
    MONGO_PORT: int = Field(env="MONGO_PORT")

    class Config:
        """
        class to represent the config for the batch process
        """
        env_file = ".env"

    def assemble_db_connection(self) -> str:
        """
        function that returns the mongo db connection string
        :return: connection string
        :rtype: str
        """
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_SERVER}:{self.MONGO_PORT}"


@lru_cache
def get_settings() -> Settings:
    """
    function to generate settings instance and cache the setting using decorator
    :return: settings
    :rtype: Settings
    """
    return Settings()
