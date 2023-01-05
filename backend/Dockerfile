FROM python:3.9-slim

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip and poetry
RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache "poetry>=1.2.2,<1.3.0"

# Create layer for dependencies
# TODO: refine this as part of CI & test updates
COPY poetry.lock pyproject.toml ./
# Create a requirements file so we can install with minimal caching
RUN poetry export --with dev \
    | grep -v '\--hash' \
    | grep -v '^torch' \
    | grep -v '^nvidia' \
    | sed -e 's/ \\$//' \
    | sed -e 's/^[[:alpha:]]\+\[\([[:alpha:]]\+\[[[:alpha:]]\+\]\)\]/\1/' \
    > requirements.txt
# The above final impenetrable sed command allows us to fix an export issue from poetry
# e.g. we need to replace pydocstyle[pydocstyle[toml]] with pydocstyle[toml]

# Install torch-cpu with pip
RUN pip3 install --no-cache "torch==1.13.0+cpu" "torchvision==0.14.0+cpu" -f https://download.pytorch.org/whl/torch_stable.html

# Install application requirements
RUN pip install --no-cache -r requirements.txt

# Download the sentence transformer model
RUN mkdir /models
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/msmarco-distilbert-dot-v5', cache_folder='/models')"

# Copy files to image
COPY . .

ENV PYTHONPATH=/app
CMD python app/main.py
