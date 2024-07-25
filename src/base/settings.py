from dotenv import find_dotenv, load_dotenv
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    db_url_scheme: str = Field(..., alias="DB_URL_SCHEME")
    db_host: str = Field(..., alias="POSTGRES_HOST")
    db_port: str = Field(..., alias="POSTGRES_PORT")
    db_name: str = Field(..., alias="POSTGRES_DB_NAME")
    db_user: str = Field(..., alias="POSTGRES_USER")
    db_password: str = Field(..., alias="POSTGRES_PASSWORD")

    @property
    def database_url(self) -> PostgresDsn:
        """ URL для подключения (DSN)"""
        return (
            f"{self.db_url_scheme}://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}?async_fallback=True"
        )


settings = Settings()
