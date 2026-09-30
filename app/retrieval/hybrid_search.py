from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import OpenAI
from config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_EMBEDDING_DEPLOYMENT,
)


search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


embedding_client = OpenAI(
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/",
    api_key=AZURE_OPENAI_API_KEY,
)


def generate_query_embedding(query: str) -> list[float]:
    response = embedding_client.embeddings.create(
    model=AZURE_EMBEDDING_DEPLOYMENT,
    input=query,
    dimensions=1536,
)

    return response.data[0].embedding


def format_search_results(results):
    documents = []

    for result in results:
        documents.append({
            "content": result.get("chunk", ""),
            "source": result.get("title", ""),
            "chunk_id": result.get("chunk_id", ""),
            "parent_id": result.get("parent_id", ""),
            "score": result.get("@search.score", 0),
        })

    return documents

def hybrid_search(query: str, top_k: int = 5):
    query_vector = generate_query_embedding(query)

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="text_vector",
        exhaustive=True,
    )

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        top=top_k,
        select=[
            "chunk",
            "title",
            "chunk_id",
            "parent_id",
        ],
    )

    return format_search_results(results)

def hyde_retrieval(hyde_answer:str,top_k: int = 5):
    hyde_vector = generate_query_embedding(hyde_answer)    
    vector_query = VectorizedQuery(
            vector=hyde_vector,
            k_nearest_neighbors=top_k,
            fields="text_vector",
            exhaustive=True,
        )

    results = search_client.search(
            vector_queries=[vector_query],
            top=top_k,
            select=[
                "chunk",
                "title",
                "chunk_id",
                "parent_id",
            ],
        )
    
    return format_search_results(results)