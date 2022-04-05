include .env
include ./makefile-local.defs
include ./makefile-docker.defs

git_hooks:
	# Install git pre-commit hooks
	cd backend/; poetry run pre-commit install --install-hooks
