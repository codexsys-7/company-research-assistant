import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

try:
    from rag.embeddings import get_collection
    from schemas.report import CompanyReport
except ModuleNotFoundError:
    from backend.rag.embeddings import get_collection
    from backend.schemas.report import CompanyReport

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"), override=True)

_llm = None


def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0,
        )
    return _llm


def _fetch_all_chunks() -> list[str]:
    """Retrieve every document stored in ChromaDB — no k limit."""
    collection = get_collection()
    if collection.count() == 0:
        return []
    result = collection.get(include=["documents"])
    docs = result.get("documents") or []
    return [d for d in docs if d]


def generate_report(company_name: str, all_context: list[str]) -> CompanyReport:
    """Generate a structured CompanyReport using all available context.

    Fetches every chunk from ChromaDB (no top-k restriction), falls back to
    the raw `all_context` list if ChromaDB is empty, then calls the LLM via
    structured output to populate every field of CompanyReport.

    Args:
        company_name: The name of the company to research.
        all_context: Raw search-result texts that were already embedded into
                     ChromaDB by the caller. Used as a fallback if ChromaDB
                     is empty at call time.

    Returns:
        A fully populated CompanyReport instance.
    """
    # 1. Pull all embedded chunks from ChromaDB; fall back to raw texts
    chroma_chunks = _fetch_all_chunks()
    context_chunks = chroma_chunks if chroma_chunks else all_context

    # 2. Join chunks with a separator so the LLM sees distinct sources
    context_block = "\n\n---\n\n".join(context_chunks)

    # 3. Build the analyst prompt
    prompt = (
        f"You are a company research analyst preparing a detailed briefing for a job candidate "
        f"who is about to interview at {company_name}.\n\n"
        f"Generate a comprehensive structured report using ONLY the context provided below. "
        f"Do not invent facts.\n\n"
        f"RULES FOR MISSING INFORMATION:\n"
        f"- String fields: write 'Information not available' when absent from context.\n"
        f"- List fields: return an EMPTY LIST [] when absent. NEVER put 'Information not available' "
        f"as a list item — that is invalid. Either populate the list or leave it empty.\n\n"
        f"FIELD-SPECIFIC GUIDANCE:\n"
        f"- tech_stack: Search for any programming languages, frameworks, cloud providers, databases, "
        f"or tools mentioned. Include inferred technologies (e.g. if the context mentions 'React app' "
        f"or 'Python API').\n"
        f"- recent_news: Look for any events, announcements, funding, product launches, layoffs, "
        f"partnerships, or leadership changes. Include up to 5 items.\n"
        f"- common_interview_questions: Extract questions that are explicitly stated or directly quoted "
        f"in the context from candidate reviews, Glassdoor, Blind, or Reddit. Do NOT paraphrase, "
        f"infer, or invent generic questions. If no specific questions appear in the context, return "
        f"an empty list.\n"
        f"- financials: Extract specific numbers from the context — annual revenue, ARR, market cap, "
        f"stock ticker and recent price, total funding raised, funding round (Series A/B/C/D), "
        f"valuation figures, IPO status, or EBITDA. Always include the year the figure refers to. "
        f"Write a 2-4 sentence paragraph summarising the financial picture. Only use "
        f"'Not publicly available' if NO financial figures appear anywhere in the context.\n"
        f"- red_flags: Look for any negative signals — layoffs, culture complaints, high turnover, "
        f"legal issues, controversies, or negative employee sentiment. Be objective, not alarmist.\n\n"
        f"CONTEXT:\n{context_block}"
    )

    # 4. Invoke LLM with structured output bound to CompanyReport schema
    llm = _get_llm()
    structured_llm = llm.with_structured_output(CompanyReport)
    report: CompanyReport = structured_llm.invoke(prompt)
    return report
