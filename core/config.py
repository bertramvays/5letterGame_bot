from pydantic import BaseSettings, SecretStr
from middlewares.words_dict import extract_words

FILE = '5_words.txt'  # путь к хранилищу слов
post_size = 250  # максимальное количество слов в одном посте.


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
words = extract_words(FILE)
