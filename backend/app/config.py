from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str = ""
    model_name: str = "gpt-4o-mini"
    upload_dir: str = "./uploads"
    vector_store_dir: str = "./data/vectorstore"


settings = Settings()
