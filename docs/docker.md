# Development using docker

Run the stack with

```shell
docker-compose up
```

The frontend should now use live-reload, and changes to code outside will restart NextJS inside the container.

## Frontend dependencies

To install packages in the running container, and also have it reflect on your host's `package*.json`:

```shell
npm run add <package name>
npm run add-dev <package name>
npm run remove <package name>
```

## Rebuilding containers

```shell
docker-compose build
```

## Restarting containers

```shell
docker-compose restart
```

## Bringing containers down

```shell
docker-compose down
```

## Logging

```shell
docker-compose logs
```

Or for a specific service:

```shell
docker-compose logs -f name_of_service # frontend|backend|db
```
