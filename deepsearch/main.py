import os
import deepsearch as ds
from deepsearch.cps.client.components.data_indices import (
    ElasticProjectDataCollectionSource,
)
from deepsearch.cps.client.components.elastic import ElasticProjectDataCollectionSource
from deepsearch.cps.queries import CorpusSemanticQuery
from deepsearch.cps.queries.results import RAGResult, SearchResult, SearchResultItem
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Annotated

import deepsearch as ds
from deepsearch.core.client.settings import ProfileSettings
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class QueryResponseResultItem(BaseModel):
    doc_hash: str
    path_in_doc: str
    passage: str
    source_is_text: bool


class QueryResponse(BaseModel):
    results: list[QueryResponseResultItem]



async def get_deepsearch_api():
    """Initialize the Deep Search Toolkit with the default env settings"""

    settings = ProfileSettings(
        username=os.getenv('USERNAME'),
        api_key=os.getenv('API_KEY'),
        host="https://sds.app.accelerate.science/",
        verify_ssl=True,
    )
    api = ds.CpsApi.from_settings(settings=settings)

    return api

@app.get("/")
async def read_root() -> dict:
    """
    Root hello world endpoint
    """
    return {"Hello": "World"}


@app.get(
    "/query",
    description="Run the semantic query on a private collection.",
)
async def query_private_documents(
    query: str,
    num_items: int = 10,
    api: ds.CpsApi = Depends(get_deepsearch_api),
) -> QueryResponse:
    """
    Run the semantic query on a private collection
    """

    proj_key = "5db97e2fe6b063d0d539b434111264c7b23c265b"
    index_key = "25592cabf6b77b90bd49ac17e8c2d44a5acfb703",

    question_query = CorpusSemanticQuery(
        question=query,
        project=proj_key,
        index_key=index_key,
        # optional params:
        retr_k=num_items,
        # text_weight=TEXT_WEIGHT,
        # rerank=RERANK,
    )
    api_output = api.queries.run(question_query)
    search_result = SearchResult.from_api_output(api_output)

    return QueryResponse(
        results=[
            QueryResponseResultItem.model_validate_json(item.json())
            for item in search_result.search_result_items
        ]
    )

