"""应用配置 - 从环境变量读取"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WicMail User Service"
    app_env: str = "development"
    database_url: str = "mysql+asyncmy://root:password@localhost:3306/wicmail"

    # JWT（与 backend-mail 共用）
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # 邮箱域名
    mailbox_domain: str = "wic.edu.kg"

    # backend-mail 服务地址，用于系统诊断和跨服务调用
    mail_service_base_url: str = "http://localhost:8000"

    # Cloudflare Email Worker 与 backend-mail 共享密钥
    cloudflare_email_secret_key: str = "change-me"

    # CORS 允许的源（逗号分隔）
    cors_origins: str = "*"

    # Cloudflare R2 附件下载配置
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "wicmail-attachments"
    r2_presign_expire_seconds: int = 3600

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
