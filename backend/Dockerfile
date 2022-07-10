FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

# Install pip and poetry
RUN pip install --upgrade pip
RUN pip install "poetry==1.1.8"

# Copy files to image
COPY ./backend .

# Install python dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Download the sentence transformer model
RUN mkdir /models
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/msmarco-distilbert-dot-v5', cache_folder='/models')"

ENV PYTHONPATH=/app

#ARG PORT=8888
#ENV PORT $PORT
#EXPOSE $PORT

CMD python app/main.py
# CMD [ "/usr/local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888", --workers 4]
