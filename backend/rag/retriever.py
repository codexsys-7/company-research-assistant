from .embeddings import get_collection


def retrieve_context(query: str, k: int = 3, company_name: str = "") -> list[str]:
    """Query ChromaDB and return the top-k most relevant document chunks.

    Args:
        query: The search query string.
        k: Number of chunks to retrieve (default 3).
        company_name: When provided, restricts results to chunks stored under
                      this company via ChromaDB metadata filtering.  This
                      prevents cross-company contamination when multiple
                      searches have been run in the same session.

    Returns:
        A list of document chunk strings, or an empty list if none found.
    """
    collection = get_collection()
    if collection.count() == 0:
        return []

    query_kwargs: dict = {
        "query_texts": [query],
        "n_results": min(k, collection.count()),
    }
    if company_name:
        query_kwargs["where"] = {"company": company_name}

    try:
        results = collection.query(**query_kwargs)
    except Exception:
        # where filter raises ValueError when no docs match the company filter.
        # Return empty — do NOT fall back to unfiltered retrieval.
        return []

    documents = results.get("documents", [[]])[0]
    return documents if documents else []
