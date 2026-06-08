"""应用配置 - 从环境变量读取"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WicMail User Service"
    app_env: str = "development"
    database_url: str = "mysql+asyncmy://wicmail:DkDTbD2kxEkS7BwW@175.178.102.49:3306/wicmail"

    # JWT（与 backend-mail 共用）
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # 邮箱域名
    mailbox_domain: str = "wic.edu.kg"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
