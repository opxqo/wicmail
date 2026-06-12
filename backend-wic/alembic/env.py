from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.config import settings
from app.database import Base
# 导入所有模型
from app.models.user import User  # noqa: F401
from app.models.mailbox import Mailbox, MailboxApplication  # noqa: F401
from app.models.email import EmailMessage, Attachment  # noqa: F401
from app.models.admin_log import AdminLog  # noqa: F401
from app.models.system_config import SystemConfig  # noqa: F401

config = context.config

# 使用 pymysql 作为同步驱动
sync_url = settings.database_url.replace("mysql+asyncmy", "mysql+pymysql")
config.set_main_option("sqlalchemy.url", sync_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        version_table="alembic_version_wic",
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_wic",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
