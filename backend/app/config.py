from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "admin"
    DB_NAME: str = "heart_craft"

    TELEGRAM_BOT_TOKEN: str = "7978181955:AAHnxHkYYXwgIWYlZqPqHIaBhs0omgevZQM"
    TELEGRAM_CHAT_ID: str = "7755699290"

    app_name: str = "Heart&Craft"
    debug: bool = True
    static_dir: str = "static"
    image_dir: str = "static/images"

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()