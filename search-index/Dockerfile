FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update

# Install pip and poetry
RUN pip install --upgrade pip
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_VERSION=1.1.13 python
ENV PATH = "${PATH}:/root/.poetry/bin"

# Copy files to image
COPY ./search-index .
# Copy common package to image
RUN mkdir /common
COPY /common ../common

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install
