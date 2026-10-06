from fastapi import FastAPI,HTTPException,APIRouter
from api.response_object import Response_Object
from pydantic import Field,BaseModel
from app.llm.query_rewriter import rewrite_query
from app.llm.prompt import build_prompt
from app.llm.service import generate_answer
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.reranker import rerank_documents
from app.llm.prompt import build_context
from app.retrieval.hybrid_search import hyde_retrieval
from app.llm.hyde import generate_hypothetical_answer
from app.agents.decide_retrieval import decide_retrieve
from app.agents.orchestrator import Orchestrator
router=APIRouter(tags=["API"])




@router.post("/get_response")
def response(response_object:Response_Object):
    query=response_object.query
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )
    k=decide_retrieve(query)
    # print(k)
    if  k:        

        rewritten_query = rewrite_query(query)
        decision=Orchestrator.orchestrate(rewritten_query)
        
        print("\nOriginal query:")
        print(query)

        print("\nRewritten query:")
        print(rewritten_query)
         
        hypothetical_answer=generate_hypothetical_answer(rewritten_query)
        print("\nHypothetical answer:")
        print(hypothetical_answer)
        
        documents = hybrid_search(rewritten_query,decision["documents"])
        print(f"\nRetrieved {len(documents)} documents.")
        h_documents=hyde_retrieval(hypothetical_answer,decision["documents"])
        
        # for i in documents:
        #     print(i)
        reranked_documents = rerank_documents(
            query=query,
            documents=documents,
            top_k=5,
        )
        
        context_documents=build_context(reranked_documents)
        #print("context documents: ",context_documents)
        print("\nReranked documents:\n")

        for i, document in enumerate(
            reranked_documents,
            start=1,
        ):
            print(f"--- Result {i} ---")
            print(f"Source: {document['source']}")
            print(f"Search score: {document['score']}")
            print(f"Rerank score: {document['rerank_score']}")
            print(document["content"][:500])
            print()

        reranked_h_documents = rerank_documents(
                query=query,
                documents=h_documents,
                top_k=5,
            )
            
        #context_h_documents=build_context(reranked_h_documents)
    else:
        rewritten_query=""
        context_documents=[]
        reranked_h_documents=[]
    prompt = build_prompt(
        query=query,
        documents=context_documents,
        h_documents=reranked_h_documents,
    )

    answer = generate_answer(prompt)

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(answer)
    if rewritten_query:
        return "Re-written query is : " + rewritten_query+ \
        "\n\nHypothetical answer:"+hypothetical_answer + \
        "\n\nReason: " + decision["reason"] + " \n\n LLM response is :"+ answer
    else:
        return " \n\n LLM response is :"+ answer 