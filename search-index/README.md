### 1. Building the docker image
The build context when building the docker image should be the parent directory of `pipeline`. This is so that common python packages can be copied to the image.

```
cd navigator
docker build -f search-index/Dockerfile -t search-indexer .
```

### 2. Creating embeddings
Use the following commands to run the pdf2text cli using model `msmarco-distilbert-dot-v5` with the default batch size and no limit. Run `docker run python /app/text2embeddings.py --help` for a full set of options.

```
docker run -v /path/to/pdf2text/outputs:/dir-in -v /path/to/output/directory:/dir-out search-indexer python /app/text2embeddings.py -i /dir-in -o /dir-out -m "msmarco-distilbert-dot-v5"
```

### 3. Loading data into Opensearch

```
docker run -v /path/to/text-ids-file:/text-ids-path -v /path/to/embeddings-file:/embeddings-path search-indexer python /app/index_data.py --text-ids-path /text-ids-path --embeddings-path /embeddings-path -d 768
```
