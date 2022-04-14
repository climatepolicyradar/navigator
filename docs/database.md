# Database migrations

Migrations are run using alembic.

# Upgrade DB with latest migrations

## Local dev environment

```
alembic upgrade head
```

## Docker dev environment

All databases:

```
make migrations
```

Or only the app-specific DBs:

```
make migrations_docker_backend
make migrations_docker_loader
```

# Create a new migration

For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## Local dev environment

In app root:

```
alembic revision --autogenerate -m "[revision message]"
```

More specifically

```
PYTHONPATH=. DATABASE_URL=postgresql://navigator:password@localhost:5432/navigator alembic revision --autogenerate -m "[revision message]"
```

## Docker dev environment

In project root:

```
make new_migration_backend "[revision message]"
```

```
make new_migration_loader "[revision message]"
```
