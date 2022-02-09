# Environment

You'd have copied `.env.example` to `.env` (either via `make dev_install`, or by hand), which includes the following environment variables:

## Postgres connection settings

The following settings will be used when setting up the Postgres server, and by the app to access the database.

- POSTGRES_USER - name of user to connect to Postgres server
- POSTGRES_PASSWORD - password of user to connect to Postgres server
- DATABASE_URL - postgres connection string - should not need to be changed for a local environment

## Admin user settings

The following superuser account will be created in the navigator database.

- SUPERUSER_EMAIL - email address of a superuser account to create to access user admin in the app
- SUPERUSER_PASSWORD - password for superuser acco