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

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: str = Field(..., env="REDIS_PORT")

    amplitude_api_key: str = Field(..., env="AMPLITUDE_API_KEY")


    class Config:
        env_file = ".env"

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
