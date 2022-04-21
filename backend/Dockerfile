FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

# Install pip and poetry
RUN pip install --upgrade pip
RUN pip install "poetry==1.1.8"

# Copy files to image
COPY ./backend .
# Copy common package to image
RUN mkdir /common
COPY ./common ../common

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Download the sentence transformer model
RUN mkdir /models
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/msmarco-distilbert-dot-v5', cache_folder='/models')"

ENV PYTHONPATH=/app

ARG PORT=8888
ENV PORT $PORT
EXPOSE $PORT

CMD python app/main.py
