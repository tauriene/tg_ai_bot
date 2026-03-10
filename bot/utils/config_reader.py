import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

env_path = pathlib.Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    bot_token: SecretStr
    ai_text_token: SecretStr
    base_webhook_url: SecretStr
    webhook_path: SecretStr
    webhook_secret: SecretStr
    debug: bool = False

    @property
    def webhook_url(self):
        return f"{self.base_webhook_url.get_secret_value()}{self.webhook_path.get_secret_value()}"

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


config = Settings()
