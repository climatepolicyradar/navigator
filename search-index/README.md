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
          "document_id" : 1297,
          "document_name" : "Full text",
          "action_id" : 1018,
          "action_date" : "02/01/2009",
          "action_name" : "National Policy for Disaster Management",
          "action_description" : "The policy recognizes that climate change contributes significantly to Kenya's increasing vulnerability to disasters in the last two decades and affects seriously the lives and livelihoods of communities. The policy therefore aims to institutionalise mechanisms to address these disasters and associated vulnerabilities stressing the central role of climate change in any sustainable and integrated National Strategy for Disaster Management.  The policy emphasises preparedness on the part of the government, communities and other stakeholders and proposes to establish and strengthen Disaster Management institutions, partnerships and networking. It proposes to mainstream Disaster Risk Reduction in the development process and strengthen the resilience of vulnerable groups.  Disaster Risk Management encompasses a full continuum from preparedness, relief and rehabilitation, mitigation and prevention including t diversification of vulnerable livelihoods and coping mechanisms. Ministry of State for Special Programmes in the Office of President is appointed as the chief national co-ordinator.",
          "action_name_and_id" : "National Policy for Disaster Management 1297",
          "action_country_code" : "KEN",
          "action_geography_english_shortname" : "Kenya",
          "action_source_name" : "CCLW",
          "action_type_name" : "Policy",
          "text_block_id" : "p0_b1",
          "text" : "GOVERNMENT OF KENYA",
          "text_embedding" : [<768xfloat>],
          "text_block_coords" : [
            [
              237.1199951171875,
              207.72000122070312
            ],
            [
              391.66815185546875,
              207.72000122070312
            ],
            [
              237.1199951171875,
              224.3520050048828
            ],
            [
              391.66815185546875,
              224.3520050048828
            ]
          ],
          "text_block_page" : 0
        }
```

**Example Opensearch document with title:**

Note the `for_search_action_name` field which is used for title search; the `action_name` field is identical to this field but appears on all documents for sorting purposes.

``` json
{
          "document_id" : 1297,
          "document_name" : "Full text",
          "action_id" : 1018,
          "action_date" : "02/01/2009",
          "action_name" : "National Policy for Disaster Management",
          "action_description" : "The policy recognizes that climate change contributes significantly to Kenya's increasing vulnerability to disasters in the last two decades and affects seriously the lives and livelihoods of communities. The policy therefore aims to institutionalise mechanisms to address these disasters and associated vulnerabilities stressing the central role of climate change in any sustainable and integrated National Strategy for Disaster Management.  The policy emphasises preparedness on the part of the government, communities and other stakeholders and proposes to establish and strengthen Disaster Management institutions, partnerships and networking. It proposes to mainstream Disaster Risk Reduction in the development process and strengthen the resilience of vulnerable groups.  Disaster Risk Management encompasses a full continuum from preparedness, relief and rehabilitation, mitigation and prevention including t diversification of vulnerable livelihoods and coping mechanisms. Ministry of State for Special Programmes in the Office of President is appointed as the chief national co-ordinator.",
          "action_name_and_id" : "National Policy for Disaster Management 1297",
          "action_country_code" : "KEN",
          "action_geography_english_shortname" : "Kenya",
          "action_source_name" : "CCLW",
          "action_type_name" : "Policy",
          "for_search_action_name" : "National Policy for Disaster Management"
        }
```

**Example text block with description:**

Note the `for_search_action_description` field and the `action_description` field - see comment about titles.

``` json
{
          "document_id" : 1297,
          "document_name" : "Full text",
          "action_id" : 1018,
          "action_date" : "02/01/2009",
          "action_name" : "National Policy for Disaster Management",
          "action_description" : "The policy recognizes that climate change contributes significantly to Kenya's increasing vulnerability to disasters in the last two decades and affects seriously the lives and livelihoods of communities. The policy therefore aims to institutionalise mechanisms to address these disasters and associated vulnerabilities stressing the central role of climate change in any sustainable and integrated National Strategy for Disaster Management.  The policy emphasises preparedness on the part of the government, communities and other stakeholders and proposes to establish and strengthen Disaster Management institutions, partnerships and networking. It proposes to mainstream Disaster Risk Reduction in the development process and strengthen the resilience of vulnerable groups.  Disaster Risk Management encompasses a full continuum from preparedness, relief and rehabilitation, mitigation and prevention including t diversification of vulnerable livelihoods and coping mechanisms. Ministry of State for Special Programmes in the Office of President is appointed as the chief national co-ordinator.",
          "action_name_and_id" : "National Policy for Disaster Management 1297",
          "action_country_code" : "KEN",
          "action_geography_english_shortname" : "Kenya",
          "action_source_name" : "CCLW",
          "action_type_name" : "Policy",
          "for_search_action_description" : "The policy recognizes that climate change contributes significantly to Kenya's increasing vulnerability to disasters in the last two decades and affects seriously the lives and livelihoods of communities. The policy therefore aims to institutionalise mechanisms to address these disasters and associated vulnerabilities stressing the central role of climate change in any sustainable and integrated National Strategy for Disaster Management.  The policy emphasises preparedness on the part of the government, communities and other stakeholders and proposes to establish and strengthen Disaster Management institutions, partnerships and networking. It proposes to mainstream Disaster Risk Reduction in the development process and strengthen the resilience of vulnerable groups.  Disaster Risk Management encompasses a full continuum from preparedness, relief and rehabilitation, mitigation and prevention including t diversification of vulnerable livelihoods and coping mechanisms. Ministry of State for Special Programmes in the Office of President is appointed as the chief national co-ordinator.",
          "action_description_embedding" : [<768xfloat>]
        }
```