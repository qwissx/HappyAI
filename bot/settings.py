from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_port: str = Field(..., env="DB_PORT")
    db_host: str = Field(..., env="DB_HOST")
    db_pass: str = Field(..., env="DB_PASS")

    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
