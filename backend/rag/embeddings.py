import sys
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Set HF token if available
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token


# --- Python 3.14 compatibility patch ---
# chromadb uses pydantic v1 internally; pydantic v1 cannot resolve annotations
# lazily (PEP 649) on Python 3.14+, causing a ConfigError on import.
# This patch catches that failure and falls back to typing.Any for those fields.
if sys.version_info >= (3, 14):
    import pydantic.v1.fields as _pvf
    from pydantic.v1 import errors as _pve
    from pydantic.v1.fields import Undefined as _Undefined
    from typing import Any as _Any

    _orig_sdat = _pvf.ModelField._set_default_and_type

    def _patched_sdat(self):
        try:
            _orig_sdat(self)
        except _pve.ConfigError:
            self.type_ = _Any
            self.outer_type_ = _Any
            self.allow_none = True
            if self.required is _Undefined:
                self.required = False
            if self.default is _Undefined:
                self.default = None

    _pvf.ModelField._set_default_and_type = _patched_sdat
# ----------------------------------------

from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"), override=True)

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

_client = None
_collection = None


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return _client


def get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = _get_client()
        embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        _collection = client.get_or_create_collection(
            name="company_data",
            embedding_function=embedding_fn,
        )
    return _collection


def chunk_text(text: str, max_words: int = 250) -> list[str]:
    """Split text into chunks of at most max_words words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words])
        if chunk:
            chunks.append(chunk)
    return chunks


def clear_collection() -> None:
    """Delete all documents from the collection."""
    collection = get_collection()
    result = collection.get(include=[])
    if result["ids"]:
        collection.delete(ids=result["ids"])


def embed_search_results(company_name: str, search_texts: list[str]) -> int:
    """
    Chunk each text at 250 words, embed all chunks, and store in ChromaDB
    with metadata {company, source}.

    Returns the total number of chunks embedded.
    """
    collection = get_collection()
    company_key = company_name.lower().replace(" ", "_")
    all_chunks = []
    all_metadatas = []
    all_ids = []

    chunk_index = 0
    for text in search_texts:
        for chunk in chunk_text(text):
            all_chunks.append(chunk)
            all_metadatas.append({"company": company_name, "source": "web_search"})
            all_ids.append(f"{company_key}_chunk_{chunk_index}")
            chunk_index += 1

    if all_chunks:
        collection.upsert(documents=all_chunks, metadatas=all_metadatas, ids=all_ids)

    return len(all_chunks)


def add_documents(texts: list[str], metadatas: list[dict]) -> None:
    collection = get_collection()
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(documents=texts, metadatas=metadatas, ids=ids)
