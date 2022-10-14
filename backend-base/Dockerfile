FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

# Install pip and poetry
RUN pip install --upgrade pip
RUN pip install "poetry==1.1.8"

# Create layer for dependencies
COPY poetry.lock pyproject.toml ./

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Download the sentence transformer model
RUN mkdir /models
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/msmarco-distilbert-dot-v5', cache_folder='/models')"
