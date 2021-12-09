git_hooks:
	# Install git pre-commit hooks
	cd backend/; poetry run pre-commit install --install-hooks

poetry_environment:
	cd backend/; poetry config virtualenvs.create false
	cd backend/; poetry install

start_containers:
	# Build and run containers
	docker-compose up -d

migrations_docker:
	# Run database migrations when using docker for development
	docker-compose run --rm backend alembic upgrade head
	# Create initial data in database
	docker-compose run --rm backend python3 app/initial_data.py

migrations_local:
	# Run database migrations in local dev mode
	cd backend/; alembic upgrade head
	# Create initial data in database
	cd backend/; python3 app/initial_data.py

dev_install:
	# Sets up a local dev environment
	# Install pip
	pip install --upgrade pip
	# Install poetry
	pip install "poetry==1.1.8"

	make poetry_environment
	make git_hooks
	make migrations_local

build: start_containers
	# Hack to wait for postgres container to be up before running alembic migrations
	sleep 5;
	# Run migrations
	make migrations_docker
	

	