# Necessary imports
from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File
from api.response_object import Response_Object
from pydantic import Field, BaseModel
from app.llm.query_rewriter import get_rewritten_query
from app.llm.prompt import build_prompt
from app.llm.service import get_answer
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.reranker import rerank_documents
from app.llm.prompt import build_context
from app.retrieval.hybrid_search import hyde_retrieval
from app.llm.hyde import get_hypothetical_answer
from app.agents.decide_retrieval import get_retrieval_decision
from app.agents.orchestrator import Orchestrator
from azure.storage.blob import BlobServiceClient
from azure.search.documents.indexes import SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
import logging

logger = logging.getLogger(__name__)
from config import (
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_STORAGE_CONTAINER1,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEXER1,
)

router = APIRouter(tags=["API"])


@router.post("/get_response")
def response(response_object: Response_Object):
    query = response_object.query
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )
    k = get_retrieval_decision(query)
    # print(k)
    if k:
        orchestrator = Orchestrator()
        rewritten_query = get_rewritten_query(query)
        decision = orchestrator.get_decision(query, rewritten_query)
        print("\nOriginal query:")
        print(query)

        print("\nRewritten query:")
        print(rewritten_query)

        hypothetical_answer = get_hypothetical_answer(rewritten_query, query)
        print("\nHypothetical answer:")
        print(hypothetical_answer)

        documents = hybrid_search(query, rewritten_query, decision["documents"])
        print(f"\nRetrieved {len(documents)} documents.")

        h_documents = (
            hyde_retrieval(hypothetical_answer, decision["documents"])
            if hypothetical_answer
            else []
        )

        # for i in documents:
        #     print(i)
        reranked_documents = rerank_documents(
            query=query,
            documents=documents,
            top_k=5,
        )

        context_documents = build_context(reranked_documents)
        # print("context documents: ",context_documents)
        print("\nReranked documents:\n")

        for i, document in enumerate(
            reranked_documents,
            start=1,
        ):
            print(f"--- Result {i} ---")
            print(f"Source: {document['source']}")
            print(f"Search score: {document['score']}")
            if document["rerank_score"]:
                print(f"Rerank score: {document['rerank_score']}")
            print(document["content"][:500])
            print()

        reranked_h_documents = rerank_documents(
            query=query,
            documents=h_documents,
            top_k=5,
        )

        # context_h_documents=build_context(reranked_h_documents)
    else:
        rewritten_query = ""
        context_documents = []
        reranked_h_documents = []
    prompt = build_prompt(
        query=query,
        documents=context_documents,
        h_documents=reranked_h_documents,
    )

    answer = get_answer(prompt)

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(answer)
    if rewritten_query:
        return (
            "Re-written query is : "
            + rewritten_query
            + "\n\nHypothetical answer:"
            + hypothetical_answer
            + "\n\nReason: "
            + decision["reason"]
            + " \n\n LLM response is :"
            + answer
        )
    else:
        return " \n\n LLM response is :" + answer


blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING
)

search_indexer_client = SearchIndexerClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


# @router.post("/upload_Technical")
@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx", ".txt", ".md"}

    filename = file.filename

    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    extension = "." + filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail="Only PDF, DOCX, TXT and MD files are supported."
        )

    try:
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER1,
            blob=filename,
        )

        file_content = await file.read()

        blob_client.upload_blob(
            file_content,
            overwrite=True,
        )
        logger.info(
            "Uploading '%s' to container '%s'",
            filename,
            AZURE_STORAGE_CONTAINER1,
        )

        blob_client.upload_blob(
            file_content,
            overwrite=True,
        )

        logger.info(
            "Blob uploaded successfully: %s",
            blob_client.url,
        )
        search_indexer_client.run_indexer(AZURE_SEARCH_INDEXER1)

        return {
            "message": "Document uploaded successfully. Indexing has been started.",
            "filename": filename,
            "indexer": AZURE_SEARCH_INDEXER1,
        }

    except Exception as e:
        logger.exception("Document upload/indexing failed")

        raise HTTPException(
            status_code=500, detail="Document upload or indexing failed."
        )
