# Frontend tests

## Local development

### Frontend unit tests

```
cd frontend
npm install
npm test
```

### Frontend e2e tests

```
cd frontend/e2e
npm install
npx cypress open
```

## Docker-based development

### Frontend unit tests

```
docker-compose run frontend test
```

This is the same as running npm test from within the frontend directory

### Frontend e2e tests

```
cd frontend/e2e
docker-compose run cypress
```

The Docker-based flow doesn't support browser UIs yet, as the steps
in [this official blog post](https://www.cypress.io/blog/2019/05/02/run-cypress-with-a-single-docker-command/#Docker-compose)
did not work.

# Backend Tests

```
docker-compose run backend pytest
```

Any arguments to pytest can also be passed after this command.

## Common errors

`TypeError: Expected a string value` could mean that you're missing an environment variable in your `.env`.
See `.env.example` for a comprehensive list of variables.