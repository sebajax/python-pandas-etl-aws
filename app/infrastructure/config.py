"""
infrastructure configuration for api
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    class to represent the infrastructure settings for the api
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
    # bucket env variables
    AWS_ACCESS_KEY: str = Field(env="AWS_ACCESS_KEY")
    AWS_SECRET_KEY: str = Field(env="AWS_SECRET_KEY")
    AWS_BUCKET_NAME: str = Field(env="AWS_BUCKET_NAME")

    class Config:
        """
        class to represent the config for the batch process
        """
        env_file = ".env"

    def assemble_db_connection(self) -> str:
        """
        :return: function that returns the mongo db connection string
        :rtype: str
        """
        mongo_uri = "mongodb+srv" if self.ENV == "test" else "mongodb"
        return f"{mongo_uri}://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_SERVER}"


@lru_cache
def get_settings() -> Settings:
    """
    :return: function to generate settings instance and cache the setting using decorator
    :rtype: Settings
    """
    return Settings()
