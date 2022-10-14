FROM 073457443605.dkr.ecr.eu-west-2.amazonaws.com/navigator-backend-base:latest

WORKDIR /app

# Create layer for dependencies
COPY poetry.lock pyproject.toml ./

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy files to image
COPY . .

ENV PYTHONPATH=/app
CMD python app/main.py
