from typing import Optional, Iterable

from opensearchpy import OpenSearch, helpers
from tqdm.auto import tqdm


class OpenSearchIndex:
    """Methods to connect to OpenSearch instance, define an index mapping, and load data into an index."""

    def __init__(
        self,
        embedding_dim: int,
        index_name: str,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        opensearch_connector_kwargs: dict = {},
    ):
        self.index_name = index_name

        self._url = url
        self._login = (username, password)
        self._opensearch_connector_kwargs = opensearch_connector_kwargs

        self.embedding_dim = embedding_dim

        self._connect_to_opensearch()

    def _connect_to_opensearch(
        self,
    ):

        if self._url:
            if all(self._login):
                self.opns = OpenSearch(
                    [self._url],
                    http_auth=self._login,
                    **self._opensearch_connector_kwargs
                )
            else:
                self.opns = OpenSearch([self._url], **self._opensearch_connector_kwargs)

        else:
            self.opns = OpenSearch(**self._opensearch_connector_kwargs)

    def is_connected(self) -> bool:
        """Check if we are connected to the OpenSearch instance."""
        return self.opns.ping()

    def _index_body(self):
        """Define policy index fields and types"""

        return {
            "settings": {
                "index": {
                    "knn": True,
                    "knn.algo_param.ef_search": 100,  # TODO: tune me. see https://opensearch.org/docs/latest/search-plugins/knn/knn-index#index-settings
                },
                "analysis": {
                    "normalizer": {
                        "lowercase_asciifold": {
                            "type": "custom",
                            "char_filter": [],
                            "filter": ["lowercase", "asciifolding"],
                        }
                    }
                },
            },
            "mappings": {
                "properties": {
                    "document_id": {"type": "keyword"},
                    "document_name": {"type": "text"},
                    "name": {
                        "type": "text",
                        "fields": {
                            "normalized": {
                                "type": "keyword",
                                "normalizer": "lowercase_asciifold",
                            }
                        },
                    },
                    "description": {"type": "text"},
                    "action_date": {"type": "date", "format": "dd/MM/yyyy"},
                    "country_code": {"type": "keyword"},
                    "action_source_name": {"type": "keyword"},
                    "action_type_name": {"type": "keyword"},
                    "text_block_id": {"type": "keyword"},
                    "text": {"type": "text"},
                    "text_embedding": {
                        "type": "knn_vector",
                        "dimension": self.embedding_dim,
                        "method": {
                            "name": "hnsw",
                            "space_type": "innerproduct",
                            "engine": "nmslib",  # TODO: decide between faiss and nmslib and tune params
                            "parameters": {
                                "ef_construction": 128,  # TODO: tune me
                                "m": 12,  # TODO: tune me
                            },
                        },
                    },
                }
            },
        }

    def delete_and_create_index(self):
        """Create the index, deleting any existing index of the same name first."""

        self.opns.indices.delete(index=self.index_name, ignore=[400, 404])
        self.opns.indices.create(index=self.index_name, body=self._index_body())

    def bulk_index(self, actions: Iterable[dict]):
        """Bulk load data into the index.

        # TODO: in future, we may want to expose `streaming_bulk` kwargs to allow for more control over the bulk load.

        Args:
            actions (Iterable[dict]): a list of documents or actions to be indexed.
        """

        actions = tqdm(actions, unit="docs")
        successes = 0

        for ok, _ in helpers.streaming_bulk(
            client=self.opns, index=self.index_name, actions=actions
        ):
            successes += ok
