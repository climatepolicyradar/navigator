# Development

You have a choice between local (host-based) or docker-based development.

## Local development

### Backend

For development on your local machine not using containers

```shell
make dev_install
```

This will install pip, poetry, git pre-commit hooks and set up a poetry environment for the backend.

It will also create an [environment](./environment.md) file at `.env`.

### Frontend

The frontend uses Node 16.13.2

```shell
cd frontend
npm install
npm start
```

This should redirect you to `http://localhost:3000`

## Docker-based development

The only dependencies for docker-based development should be docker and docker-compose.

Firstly, copy the sample [environment](./environment.md) file:

```shell
cp .env.example .env
```

Then run the following command:

```shell
make start
make show_logs
```

This will build and bring up the containers, run database migrations and populate the database with initial data.

## Running services

The backend will be at `http://localhost:8000`

Auto-generated docs will be at `http://localhost:8000/api/docs`

The frontend will be at `http://localhost:3000`

## Common issues

### Tests pass locally, but not on CI

CI uses docker, so ensure all containers are built with latest dependencies, and all tests pass:

```shell
make build
make test
```

Missing code might be

- ignored by `.gitignore` and not be seen/found by CI
- ignored by `.dockerignore` and not be seen/found by the containers

## Further information

- [environment](./environment.md)
- [testing](./testing.md)
- [vscode](./vscode.md)
