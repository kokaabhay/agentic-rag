from azure.search.documents.indexes import SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()
AZURE_SEARCH_INDEXER1 = os.getenv("AZURE_SEARCH_INDEXER1")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

search_indexer_client = SearchIndexerClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def run_indexer():
    print(f"Running indexer: {AZURE_SEARCH_INDEXER1}")

    search_indexer_client.run_indexer(AZURE_SEARCH_INDEXER1)

    print("Indexer started successfully.")


if __name__ == "__main__":
    run_indexer()
