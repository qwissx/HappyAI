from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str

    db_name: str
    db_user: str
    db_port: str
    db_host: str
    db_pass: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
