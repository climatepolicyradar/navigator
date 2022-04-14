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
make upgrade_all_dbs
```

Or only the app-specific DBs:

```
make upgrade_loader_db
make upgrade_backend_db
```

# Create a new migration

For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## Local dev environment

```
alembic revision --autogenerate -m "[revision message]"
```

More specifically

```
PYTHONPATH=. DATABASE_URL=postgresql://navigator:password@localhost:5432/navigator alembic revision --autogenerate -m "[revision message]"
```

## Docker dev environment

```
docker-compose run --rm backend alembic revision --autogenerate -m "[revision message]"
```
