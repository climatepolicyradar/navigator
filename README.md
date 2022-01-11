![backend and frontend tests](https://github.com/climatepolicyradar/navigator/actions/workflows/test.yml/badge.svg)

# Climate Policy Radar Navigator

## Development

The only dependencies for this project should be docker and docker-compose.

### Environment variables
To set up a local or docker-based development environment, you need to set up a few environment variables first. To files are provided for reference:

- `.env.template` - template environment file showing required environment variables
- `.env.example`  - example environment file with example values for each of the environment variables.

Create a `.env` file in the root of the project by copying the `.env.template` file, or using the example file for reference. The following variables should be specified:

#### Postgres connection settings

The following settings will be used when setting up the Postgres server, and by the app to access the database.

- POSTGRES_USER - name of user to connect to Postgres server
- POSTGRES_PASSWORD - password of user to connect to Postgres server
- DATABASE_URL - postgres connection string - should not need to be changed for a local environment

#### Admin user settings

The following superuser account will be created in the navigator database.

- SUPERUSER_EMAIL - email address of a superuser account to create to access user admin in the app
- SUPERUSER_PASSWORD - password for superuser account

### Development using vscode and containers.

For development inside docker containers using vscode, run the following command:

```bash
make build
```

This will build and bring up the containers, run database migrations and populate the database with initial data.

And navigate to http://localhost:8000

Auto-generated docs will be at
http://localhost:8000/api/docs

#### VSCode development container

Open the project locally in vscode. It should detect that the project is configured to use a dev container 
and prompt to open the project in the container. Note that it is configured for backend development. If you wish to use the front end container for development instead, you need to update `.devcontainer/devcontainer.json` with the following setting:

```
"service": "frontend"
```

### Local development

For development on your local machine not using containers

```bash
make dev_install
```

This will install pip, poetry, git pre-commit hooks and set up a poetry environment for the backend.

### Rebuilding containers:

```
docker-compose build
```

### Restarting containers:

```
docker-compose restart
```

### Bringing containers down:

```
docker-compose down
```

### Frontend Development

Alternatively to running inside docker, it can sometimes be easier
to use npm directly for quicker reloading. To run using npm:

```
cd frontend
npm install
npm start
```

This should redirect you to http://localhost:3000

### Frontend Tests

```
cd frontend
npm install
npm test
```

## Database migrations

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

## Testing

There is a helper script for both frontend and backend tests:

```
./scripts/test.sh
```

### Backend Tests

```
docker-compose run backend pytest
```

any arguments to pytest can also be passed after this command

### Frontend Tests

```
docker-compose run frontend test
```

This is the same as running npm test from within the frontend directory

## Logging

```
docker-compose logs
```

Or for a specific service:

```
docker-compose logs -f name_of_service # frontend|backend|db
```