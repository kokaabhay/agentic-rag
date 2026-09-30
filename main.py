from fastapi import FastAPI,HTTPException
from api.routes import router
app=FastAPI(title="RAG using Azure",description="basic RAG Pipeline using Azure search service and Foundry")

app.include_router(router)


@app.get("/health")
def get_health():
    status="OK"
    return {"status":status}

# def main():
#     query = input("Ask a question: ")

#     rewritten_query = rewrite_query(query)

#     print("\nOriginal query:")
#     print(query)

#     print("\nRewritten query:")
#     print(rewritten_query)

#     documents = hybrid_search(rewritten_query)

#     print(f"\nRetrieved {len(documents)} documents.")
#     # for i in documents:
#     #     print(i)
#     reranked_documents = rerank_documents(
#         query=query,
#         documents=documents,
#         top_k=5,
#     )
    
#     context_documents=build_context(reranked_documents)
#     #print("context documents: ",context_documents)
#     print("\nReranked documents:\n")

#     for i, document in enumerate(
#         reranked_documents,
#         start=1,
#     ):
#         print(f"--- Result {i} ---")
#         print(f"Source: {document['source']}")
#         print(f"Search score: {document['score']}")
#         print(f"Rerank score: {document['rerank_score']}")
#         print(document["content"][:500])
#         print()

#     prompt = build_prompt(
#         query=query,
#         documents=context_documents,
#     )

#     answer = generate_answer(prompt)

#     print("\n" + "=" * 60)
#     print("FINAL ANSWER")
#     print("=" * 60)
#     print(answer)


# if __name__ == "__main__":
#     main()

