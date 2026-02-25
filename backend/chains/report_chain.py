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


def answer_query(query: str, context: list[str]) -> str:
    """Generate an answer using OpenAI based on retrieved context chunks.

    Args:
        query: The user's question.
        context: List of relevant document chunks from ChromaDB.

    Returns:
        OpenAI's synthesized answer as a string.
    """
    context_block = "\n\n".join(context)
    prompt = (
        f"Context:\n{context_block}\n\n"
        f"Question: {query}\n\n"
        "Answer based only on the context provided above."
    )
    llm = _get_llm()
    response = llm.invoke(prompt)
    return response.content
