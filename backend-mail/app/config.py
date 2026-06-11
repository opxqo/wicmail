"""应用配置 - 从环境变量读取"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WicMail Backend"
    app_env: str = "development"
    cloudflare_email_secret_key: str = "change-me"
    database_url: str = "mysql+asyncmy://root:password@localhost:3306/wicmail"

    # JWT 配置
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 小时

    # 默认管理员（首次启动时自动创建）
    default_admin_username: str = "admin"
    default_admin_password: str = "admin123456"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
