# Opensearch Indexer

The code in this folder contains multiple CLIs used to index data into the Navigator search index:
* `text2embeddings.py`: loads JSON data produced by the `pdf2text` pipeline and converts it to embeddings (.memmap) and text and IDs (.json) files.
* `index_data.py`: loads document metadata from the Navigator database and the prototype *processed_policies.csv** file and indexes this data alongside the text and embeddings created using `text2embeddings` into the search index.

There is also an `opensearch-query-example.ipynb` notebook that demonstrates running a query on the index. This is to be developed further and integrated into the Navigator APIs.

## Running
### 1. Building

Build using `docker-compose`: see [quickstart](../docs/quickstart.md).

### 2. Creating embeddings
Use the following command to run the pdf2text cli using model `msmarco-distilbert-dot-v5` with the default batch size and no limit. Run `docker-compose run search-index python /app/text2embeddings.py --help` for a full set of options.

> :warning: this command currently fails with a memory error in docker-compose, but works fine when run on Python directly on the host machine. To get this running you can `poetry install` this folder and pass the database URL directly to python.
> e.g. `DATABASE_URL=postgres://blabla poetry run python /app/text2embeddings.py --args`
> This has been raised as a [bug issue](https://github.com/climatepolicyradar/navigator/issues/438).

```
docker-compose run -v /path/to/pdf2text/outputs:/dir-in -v /path/to/output/directory:/dir-out search-index python /app/text2embeddings.py -i /dir-in -o /dir-out -m "msmarco-distilbert-dot-v5"
```

### 3. Loading data into Opensearch (in docker-compose)

Note: this command will wipe and repopulate the index specified in `.env` if it's already populated.

```
docker-compose run -v /path/to/text-ids-file:/text-ids-path -v /path/to/embeddings-file:/embeddings-path search-index python /app/index_data.py --text-ids-path /text-ids-path --embeddings-path /embeddings-path -d 768
```
