# Frontend tests

## Local development

```
cd frontend
npm install
npm test
```

## Docker-based development

```
docker-compose run frontend test
```

This is the same as running npm test from within the frontend directory

# Backend Tests

```
docker-compose run backend pytest
```

Any arguments to pytest can also be passed after this command.
