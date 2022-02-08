# Database migrations

Migrations are run using alembic. To run all migrations:

Local dev environment:
```
alembic upgrade head
```

Docker dev environment:
```
docker-compose run --rm backend alembic upgrade head
```

To create a new migration:

```
alembic revision -m "[revision _name]"
```

And fill in `upgrade` and `downgrade` methods. For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).
