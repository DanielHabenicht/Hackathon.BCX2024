import os
import deepsearch as ds
from deepsearch.cps.client.components.data_indices import (
    ElasticProjectDataCollectionSource,
)
from deepsearch.cps.client.components.elastic import ElasticProjectDataCollectionSource
from deepsearch.cps.queries import CorpusRAGQuery
from deepsearch.cps.queries.results import RAGResult, SearchResult, SearchResultItem
from fastapi import Depends, FastAPI, Response, HTTPException, status
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
    index_key = "25592cabf6b77b90bd49ac17e8c2d44a5acfb703"

    print(query)
    # submit natural-language query on collection
    question_query = CorpusRAGQuery(
        question=query,
        project=proj_key,
        index_key=index_key,
    )
    api_output = api.queries.run(question_query)
    rag_result = RAGResult.from_api_output(api_output)
    
    return Response(content=rag_result.json(), media_type="application/json")

