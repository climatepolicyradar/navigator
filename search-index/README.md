### 1. Building the docker image

Build using `docker-compose`: see [quickstart](../docs/quickstart.md).

### 2. Creating embeddings
Use the following commands to run the pdf2text cli using model `msmarco-distilbert-dot-v5` with the default batch size and no limit. Run `docker-compose run search-index python /app/text2embeddings.py --help` for a full set of options.

```
docker-compose run -v /path/to/pdf2text/outputs:/dir-in -v /path/to/output/directory:/dir-out search-index python /app/text2embeddings.py -i /dir-in -o /dir-out -m "msmarco-distilbert-dot-v5"
```

### 3. Loading data into Opensearch (in docker-compose)

Note: this command will wipe and repopulate the index specified in `.env` if it's already populated.

```
docker-compose run -v /path/to/text-ids-file:/text-ids-path -v /path/to/embeddings-file:/embeddings-path search-index python /app/index_data.py --text-ids-path /text-ids-path --embeddings-path /embeddings-path -d 768
```
