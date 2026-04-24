from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.session import Base
import os
import pkgutil
import importlib

# Dynamically import all 'models' submodules in 'app.modules'
def import_all_models():
    import app.modules as modules_pkg
    # walk_packages looks into subdirectories of app.modules
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        modules_pkg.__path__, modules_pkg.__name__ + "."
    ):
        # Only import if the submodule ends with '.models'
        if module_name.endswith(".models"):
            importlib.import_module(module_name)
import_all_models()

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def get_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/app"
    )


def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        url=get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
