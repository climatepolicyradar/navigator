# Database migrations

Migrations are run using alembic.

# Upgrade DB with latest migrations

## Local dev environment

```
alembic upgrade head
```

## Docker dev environment

```
docker-compose run --rm backend alembic upgrade head
```

# Create a new migration

For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## Local dev environment

```
alembic revision --autogenerate -m "[revision message]"
```

## Docker dev environment

```
docker-compose run --rm backend alembic revision --autogenerate -m "[revision message]"
```
