from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    agila_db_hostname: str
    agila_db_port: str
    agila_db_password: str
    agila_db_name: str
    agila_db_username: str
    agila_secret_key: str
    agila_algorithm: str
    agila_access_token_expire_minutes: int
    pythonunbuffered: int
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
