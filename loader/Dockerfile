FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

# Install pip and poetry
RUN pip install --upgrade pip
RUN pip install "poetry==1.1.13"

# Copy files to image
COPY . .

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install