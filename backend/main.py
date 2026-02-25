import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.embeddings import clear_collection, embed_search_results
from rag.retriever import retrieve_context
from chains.report_chain import answer_query
from search.duckduckgo_client import search_company, process_results

logger = logging.getLogger(__name__)

app = FastAPI(title="Company Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    company_name: str
    query: str


@app.get("/")
def hello_world():
    return {"message": "Hello from Company Research Assistant!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/research")
def research(request: ResearchRequest):
    # 1. Clear stale data
    try:
        clear_collection()
    except Exception as e:
        logger.error("ChromaDB clear failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Vector store error: {e}")

    # 2. Fetch live web results for the company
    try:
        raw_results = search_company(request.company_name)
    except Exception as e:
        logger.error("Web search failed for '%s': %s", request.company_name, e)
        raise HTTPException(status_code=503, detail=f"Web search error: {e}")

    if not raw_results:
        raise HTTPException(
            status_code=404,
            detail=f"No web results found for '{request.company_name}'. Check the company name and try again.",
        )

    # 3. Deduplicate and clean
    search_texts = process_results(raw_results)

    # 4. Embed into ChromaDB
    try:
        chunks_embedded = embed_search_results(request.company_name, search_texts)
    except Exception as e:
        logger.error("ChromaDB embed failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Vector store error: {e}")

    # 5. Retrieve relevant context for the query
    try:
        context = retrieve_context(request.query)
    except Exception as e:
        logger.error("ChromaDB retrieval failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Vector store error: {e}")

    if not context:
        raise HTTPException(status_code=404, detail="No relevant context found for this query.")

    # 6. Generate answer
    try:
        answer = answer_query(request.query, context)
    except Exception as e:
        logger.error("LLM call failed: %s", e)
        raise HTTPException(status_code=503, detail=f"LLM error: {e}")

    return {
        "status": "ok",
        "company": request.company_name,
        "query": request.query,
        "answer": answer,
        "sources_found": len(raw_results),
        "chunks_embedded": chunks_embedded,
    }
