import logging
import os
from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.db.models import Base

logger = logging.getLogger(__name__)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if "SKIP_ALEMBIC_LOGGING" not in os.environ.keys():
    fileConfig(config.config_file_name, disable_existing_loggers=False)  # type: ignore

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    db_url = os.environ["DATABASE_URL"]
    return db_url


def generate_incremental_revision_id(context, revision, directives) -> None:
    if getattr(context.config.cmd_opts, "autogenerate", False):
        script = directives[0]
        # current version
        cur_rev = max([int(rev) for rev in context.get_current_heads()], default=0)
        # force new version
        script.rev_id = "{:04d}".format(cur_rev + 1)
        if script.upgrade_ops.is_empty():
            directives[:] = []
            logger.info("No changes in schema detected.")
        elif not script.message:
            directives[:] = []
            logger.info("Message not provided - can not create revision.")
            logger.info("Run script with -m MESSAGE or --message MESSAGE")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        raise RuntimeError("Alembic section of configuration is missing")
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=generate_incremental_revision_id,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
