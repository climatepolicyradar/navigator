# Development using docker

Run the stack with

```
docker-compose up
```

The frontend should now use live-reload, and changes to code outside will restart NextJS inside the container.

# Frontend dependencies

To install packages in the running container, and also have it reflect on your host's `package*.json`:

```
npm run add <package name>
npm run add-dev <package name>
npm run remove <package name>
```

# Rebuilding containers:

```
docker-compose build
```

# Restarting containers:

```
docker-compose restart
```

# Bringing containers down:

```
docker-compose down
```

# Logging

```
docker-compose logs
```

Or for a specific service:

```
docker-compose logs -f name_of_service # frontend|backend|db
```