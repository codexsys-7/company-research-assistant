from .embeddings import get_collection


def retrieve_context(query: str, k: int = 3) -> list[str]:
    """Query ChromaDB and return the top-k most relevant document chunks.

    Args:
        query: The search query string.
        k: Number of chunks to retrieve (default 3).

    Returns:
        A list of document chunk strings, or an empty list if none found.
    """
    collection = get_collection()
    if collection.count() == 0:
        return []

    results = collection.query(query_texts=[query], n_results=min(k, collection.count()))
    documents = results.get("documents", [[]])[0]
    return documents if documents else []
