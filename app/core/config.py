from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_version: str
    database_url: str
    geo_api_url: str
    geo_api_token: str

    class Config:
        env_file = '.env'


settings = Settings()
