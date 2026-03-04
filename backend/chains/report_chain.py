import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"), override=True)

_llm = None


def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    return _llm


def is_real_company(company_name: str) -> bool:
    """Ask the LLM whether the given name is a real company."""
    llm = _get_llm()
    response = llm.invoke(
        f"Is '{company_name}' a real, identifiable company or organisation "
        f"(including startups, private companies, and nonprofits)? "
        f"Reply with only YES or NO."
    )
    return response.content.strip().upper().startswith("YES")


def answer_query(query: str, context: list[str], company_name: str = "") -> str:
    """Generate an answer using OpenAI based on retrieved context chunks.

    Args:
        query: The user's question.
        context: List of relevant document chunks from ChromaDB.
        company_name: The company being researched (used to anchor the answer).

    Returns:
        OpenAI's synthesized answer as a string.
    """
    context_block = "\n\n".join(context)
    company_clause = f" about {company_name}" if company_name else ""
    no_info_reply = (
        f"I don't have specific information{company_clause} on this topic in my research data."
    )
    prompt = (
        f"You are a research assistant answering questions{company_clause}.\n\n"
        f"Context from web research:\n{context_block}\n\n"
        f"Question: {query}\n\n"
        f"Instructions:\n"
        f"- Answer using ONLY the context provided above.\n"
        f"- If the context does not contain information specifically{company_clause} for this question, "
        f"respond with exactly: \"{no_info_reply}\"\n"
        f"- Do NOT use general knowledge or information about other companies."
    )
    llm = _get_llm()
    response = llm.invoke(prompt)
    return response.content
