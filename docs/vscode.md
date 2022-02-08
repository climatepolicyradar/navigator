# VSCode development container

Open the project locally in vscode. It should detect that the project is configured to use a dev container 
and prompt to open the project in the container. Note that it is configured for backend development. If you wish to use the front end container for development instead, you need to update `.devcontainer/devcontainer.json` with the following setting:

```
"service": "frontend"
```