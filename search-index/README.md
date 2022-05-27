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

> WARNING: this command currently fails with a memory error in docker-compose, but works fine when run on Python directly on the host machine. To get this running you can `poetry install` this folder and pass the database URL directly to python.
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
## Opensearch index structure

The following snippets are examples of the structure of different documents in the Opensearch index. Each document in the Opensearch index either describes a title, a description, or a text block of a document. **TODO: This will be revised once we remove the concept of actions from our database.**

**Example opensearch document with text block:**

``` json
{
    "md5_sum" : "1c11e58a696ca5741fdc3454b4369564",
    "document_url" : "https://cdn.climatepolicyradar.org/PHL/2020/PHL-2020-03-19-Sustainable Finance Policy Framework of 2020-319_1c11e58a696ca5741fdc3454b4369564.pdf",
    "document_id" : 167,
    "document_name" : "Sustainable Finance Policy Framework of 2020",
    "document_date" : "19/03/2020",
    "document_description" : "This document was approved by circular 1085/2020 of Philippines' central bank. It defines the bank's vision to integrate sustainability principles in corporate governance and risk management frameworks as well as in strategic objectives of banks.&nbsp;",
    "document_category" : "Policy",
    "document_type" : "Framework",
    "document_keyword" : [
      "Finance",
      "Central Bank"
    ],
    "document_sector_name" : "Finance",
    "document_hazard_name" : [ ],
    "document_instrument_name" : [
      "Processes, plans and strategies|Governance",
      "Capacity building|Governance"
    ],
    "document_language" : "English",
    "document_instrument_parent" : [ ],
    "document_framework_name" : [ ],
    "document_response_name" : [
      "Mitigation",
      "Adaptation"
    ],
    "document_name_and_id" : "Sustainable Finance Policy Framework of 2020 167",
    "document_country_code" : "PHL",
    "document_country_english_shortname" : "Philippines",
    "document_region_english_shortname" : "East Asia & Pacific",
    "document_region_code" : "East Asia & Pacific",
    "document_source_name" : "CCLW",
    "text_block_id" : "p0_b1",
    "text" : "CIRCULAR NO. 1085",
    "text_embedding" : [x768],
    "text_block_coords" : [
      [
        263.2799987792969,
        709.3638153076172
      ],
      [
        364.5785827636719,
        709.3638153076172
      ],
      [
        364.5785827636719,
        720.4228668212891
      ],
      [
        263.2799987792969,
        720.4228668212891
      ]
    ],
    "text_block_page" : 0
}
```

**Example Opensearch document with title:**

Note the `for_search_document_name` field which is used for title search; the `document_name` field is identical to this field but appears on all documents for sorting purposes.

``` json
{
  "md5_sum" : "1c11e58a696ca5741fdc3454b4369564",
  "document_url" : "https://cdn.climatepolicyradar.org/PHL/2020/PHL-2020-03-19-Sustainable Finance Policy Framework of 2020-319_1c11e58a696ca5741fdc3454b4369564.pdf",
  "document_id" : 167,
  "document_name" : "Sustainable Finance Policy Framework of 2020",
  "document_date" : "19/03/2020",
  "document_description" : "This document was approved by circular 1085/2020 of Philippines' central bank. It defines the bank's vision to integrate sustainability principles in corporate governance and risk management frameworks as well as in strategic objectives of banks.&nbsp;",
  "document_category" : "Policy",
  "document_type" : "Framework",
  "document_keyword" : [
    "Finance",
    "Central Bank"
  ],
  "document_sector_name" : "Finance",
  "document_hazard_name" : [ ],
  "document_instrument_name" : [
    "Processes, plans and strategies|Governance",
    "Capacity building|Governance"
  ],
  "document_language" : "English",
  "document_instrument_parent" : [ ],
  "document_framework_name" : [ ],
  "document_response_name" : [
    "Mitigation",
    "Adaptation"
  ],
  "document_name_and_id" : "Sustainable Finance Policy Framework of 2020 167",
  "document_country_code" : "PHL",
  "document_country_english_shortname" : "Philippines",
  "document_region_english_shortname" : "East Asia & Pacific",
  "document_region_code" : "East Asia & Pacific",
  "document_source_name" : "CCLW",
  "for_search_document_name" : "Sustainable Finance Policy Framework of 2020"
}
```

**Example text block with description:**

Note the `for_search_document_description` field and the `document_description` field - see comment about titles.

``` json
{
  "md5_sum" : "1c11e58a696ca5741fdc3454b4369564",
  "document_url" : "https://cdn.climatepolicyradar.org/PHL/2020/PHL-2020-03-19-Sustainable Finance Policy Framework of 2020-319_1c11e58a696ca5741fdc3454b4369564.pdf",
  "document_id" : 167,
  "document_name" : "Sustainable Finance Policy Framework of 2020",
  "document_date" : "19/03/2020",
  "document_description" : "This document was approved by circular 1085/2020 of Philippines' central bank. It defines the bank's vision to integrate sustainability principles in corporate governance and risk management frameworks as well as in strategic objectives of banks.&nbsp;",
  "document_category" : "Policy",
  "document_type" : "Framework",
  "document_keyword" : [
    "Finance",
    "Central Bank"
  ],
  "document_sector_name" : "Finance",
  "document_hazard_name" : [ ],
  "document_instrument_name" : [
    "Processes, plans and strategies|Governance",
    "Capacity building|Governance"
  ],
  "document_language" : "English",
  "document_instrument_parent" : [ ],
  "document_framework_name" : [ ],
  "document_response_name" : [
    "Mitigation",
    "Adaptation"
  ],
  "document_name_and_id" : "Sustainable Finance Policy Framework of 2020 167",
  "document_country_code" : "PHL",
  "document_country_english_shortname" : "Philippines",
  "document_region_english_shortname" : "East Asia & Pacific",
  "document_region_code" : "East Asia & Pacific",
  "document_source_name" : "CCLW",
  "for_search_document_description" : "This document was approved by circular 1085/2020 of Philippines' central bank. It defines the bank's vision to integrate sustainability principles in corporate governance and risk management frameworks as well as in strategic objectives of banks.&nbsp;",
  "document_description_embedding" : [x768],
}
```

# Common issues

## Virtual memory

Error in docker logs:

```
opensearch-node1          | ERROR: [2] bootstrap checks failed
opensearch-node1          | [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
opensearch-node1          | [2]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
opensearch-node1          | ERROR: OpenSearch did not exit normally - check the logs at /usr/share/opensearch/logs/opensearch-cluster.log
opensearch-node1          | [2022-04-14T14:49:58,972][INFO ][o.o.n.Node               ] [opensearch-node1] stopping ...
opensearch-node1          | [2022-04-14T14:49:58,985][INFO ][o.o.n.Node               ] [opensearch-node1] stopped
opensearch-node1          | [2022-04-14T14:49:58,985][INFO ][o.o.n.Node               ] [opensearch-node1] closing ...
opensearch-node1          | [2022-04-14T14:49:58,995][INFO ][o.o.n.Node               ] [opensearch-node1] closed
opensearch-node1          | Killing performance analyzer process 34
opensearch-node1          | OpenSearch exited with code 78
opensearch-node1          | Performance analyzer exited with code 143
```

Run [this command](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html) on the host machine:

``` 
sysctl -w vm.max_map_count=262144
```