# Import the deepsearch-toolkit
import deepsearch as ds
from deepsearch.cps.client.components.data_indices import (
    ElasticProjectDataCollectionSource,
)
from deepsearch.cps.client.api import CpsApi
from deepsearch.cps.client.components.elastic import ElasticProjectDataCollectionSource
from deepsearch.cps.queries import DataQuery, CorpusRAGQuery, CorpusSemanticQuery
from deepsearch.cps.queries.results import RAGResult, SearchResult, SearchResultItem

import pandas as pd

PROJ_KEY = "5db97e2fe6b063d0d539b434111264c7b23c265b"
INDEX_KEY = "25592cabf6b77b90bd49ac17e8c2d44a5acfb703"

settings = ProfileSettings(
    username="",
    api_key="",
    host="https://sds.app.accelerate.science/",
    verify_ssl=True,
)
api = CpsApi.from_settings(settings=settings)

coll_coords = ElasticProjectDataCollectionSource(
    proj_key=PROJ_KEY,
    index_key=INDEX_KEY,
)

# Prepare the data query
query = DataQuery(
    search_query="*",  # The search query to be executed
    source=[           # Which fields of documents we want to fetch
            "file-info.document-hash",
            "file-info.filename",
            # "description.title",
    ],
    coordinates=coll_coords,  # The data collection to be queries
)

# Query Deep Search for the documents matching the query
results = []
query_results = api.queries.run(query)
for row in query_results.outputs["data_outputs"]:
        # Add row to results table
        results.append({
            "Filename": row["_source"]["file-info"]["filename"],
            "DocHash": row["_source"]["file-info"]["document-hash"],
            # "Title": row["_source"].get("description", {}).get("title"),
        })

print(f'Finished fetching all data. Total is {len(results)} records.')

# Visualize the table with all results
# df = pd.json_normalize(results)
# df

# Do only once
from deepsearch.cps.client.components.documents import SemIngestPrivateDataCollectionSource

# launch the ingestion of the collection for DocumentQA
task = api.documents.semantic_ingest(
    project=PROJ_KEY,
    data_source=SemIngestPrivateDataCollectionSource(
        source=coll_coords,
    ),
)

# wait for the ingestion task to finish
api.tasks.wait_for(task.proj_key, task.task_id)

question = "Where is the IBM lab in Zurich?"

# submit natural-language query on collection
question_query = CorpusRAGQuery(
    question=question,
    project=PROJ_KEY,
    index_key=INDEX_KEY,
)
api_output = api.queries.run(question_query)
rag_result = RAGResult.from_api_output(api_output)

print(rag_result)