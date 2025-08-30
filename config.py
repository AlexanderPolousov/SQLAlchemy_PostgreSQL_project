import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
#__file__ - путь к текущему файлу Python
# os.path.abspath(__file__) - получает абсолютный путь к файлу
# os.path.dirname() - получает директорию, где лежит файл
# os.path.join() - соединяет путь к директории с именем файла .env
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()


# print("DB URL =>", settings.get_db_url())
# print("DB HOST =>", settings.DB_HOST)

