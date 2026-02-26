import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.embeddings import clear_collection, embed_search_results
from rag.retriever import retrieve_context
from chains.report_chain import answer_query
from agents.research_graph import build_graph

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


research_graph = build_graph()


@app.post("/research")
def research(request: ResearchRequest):
    start_time = time.time()

    # 1. Clear stale data
    try:
        clear_collection()
    except Exception as e:
        logger.error("ChromaDB clear failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Vector store error: {e}")

    # 2. Run LangGraph agent (parallel news/culture/tech/interview → aggregator)
    try:
        initial_state = {
            "company_name": request.company_name,
            "news_results": [],
            "culture_results": [],
            "tech_results": [],
            "interview_results": [],
            "all_results": [],
        }
        final_state = research_graph.invoke(initial_state)
        search_texts = final_state["all_results"]
    except Exception as e:
        logger.error("Agent graph failed for '%s': %s", request.company_name, e)
        raise HTTPException(status_code=503, detail=f"Research agent error: {e}")

    if not search_texts:
        raise HTTPException(
            status_code=404,
            detail=f"No web results found for '{request.company_name}'. Check the company name and try again.",
        )

    # 3. Embed into ChromaDB
    try:
        chunks_embedded = embed_search_results(request.company_name, search_texts)
    except Exception as e:
        logger.error("ChromaDB embed failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Vector store error: {e}")

    # 4. Retrieve relevant context for the query
    try:
        context = retrieve_context(request.query)
    except Exception as e:
        logger.error("ChromaDB retrieval failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Vector store error: {e}")

    if not context:
        raise HTTPException(status_code=404, detail="No relevant context found for this query.")

    # 5. Generate answer
    try:
        answer = answer_query(request.query, context)
    except Exception as e:
        logger.error("LLM call failed: %s", e)
        raise HTTPException(status_code=503, detail=f"LLM error: {e}")

    elapsed = round(time.time() - start_time, 2)

    return {
        "status": "ok",
        "company": request.company_name,
        "query": request.query,
        "answer": answer,
        "sources_found": len(search_texts),
        "chunks_embedded": chunks_embedded,
        "execution_time_s": elapsed,
    }
