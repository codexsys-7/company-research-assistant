from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.retriever import retrieve_context
from chains.report_chain import answer_query

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
    context = retrieve_context(request.query)
    if not context:
        raise HTTPException(status_code=404, detail="No relevant context found for this query.")
    answer = answer_query(request.query, context)
    return {"answer": answer}
