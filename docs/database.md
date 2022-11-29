# Database migrations

Migrations are run using alembic.

## Upgrade DB with latest migrations

### Local dev environment

```shell
alembic upgrade head
```

### Docker dev environment

All databases:

```shell
make migrations
```

Or only the app-specific DBs:

```shell
make migrations_docker_backend
make migrations_docker_loader
```

## Create a new migration

For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

### Local dev environment

In app root:

```shell
alembic revision --autogenerate -m "[revision message]"
```

More specifically

```shell
PYTHONPATH=. DATABASE_URL=postgresql://navigator:password@localhost:5432/navigator alembic revision --autogenerate -m "[revision message]"
```

### Docker dev environment

In project root:

```shell
make new_migration_backend "[revision message]"
```

```shell
make new_migration_loader "[revision message]"
```
