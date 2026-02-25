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

# ---------------------------------------------------------------------------
# Hardcoded Stripe data for Phase 1 testing
# ---------------------------------------------------------------------------
STRIPE_DATA = """
Stripe is a financial infrastructure platform for businesses of all sizes. Founded in 2010 \
by brothers Patrick Collison and John Collison, the company was born out of a simple \
observation: accepting payments on the internet was far too difficult for most businesses. \
Starting from a small San Francisco apartment, Stripe quickly gained traction among developers \
for its clean, intuitive APIs and comprehensive documentation. Today, Stripe processes hundreds \
of billions of dollars in payments annually and serves millions of businesses in over 100 \
countries, ranging from small startups to large public enterprises such as Amazon, Google, \
and Salesforce.

Stripe's product portfolio has expanded well beyond basic payment processing. Its core \
offering, Stripe Payments, supports over 135 currencies and dozens of payment methods \
including cards, bank transfers, and local payment schemes. Stripe Billing handles recurring \
revenue and subscription management for SaaS businesses. Stripe Connect powers marketplace \
and platform businesses by routing funds between multiple parties. Stripe Terminal extends \
payment acceptance to physical retail with programmable card readers. Additional products \
include Stripe Radar for machine-learning-based fraud detection, Stripe Issuing for creating \
custom debit and credit cards, and Stripe Treasury for embedding financial services directly \
into software platforms.

On the engineering side, Stripe is known for its polyglot technical culture. The company \
uses Ruby for many backend services and Scala for high-throughput data pipelines. The \
frontend is built primarily with React and TypeScript. Data is stored across MongoDB, MySQL, \
and Redis depending on the use case. Stripe invests heavily in internal developer tooling, \
including a sophisticated monorepo setup, automated testing infrastructure, and custom \
deployment systems. The engineering blog regularly publishes deep technical posts covering \
distributed systems design, compiler optimisations, and reliability engineering.

Stripe consistently ranks among the best engineering workplaces in the world. The company \
places a high premium on writing — both internal documentation and external communication — \
believing that clear writing reflects clear thinking. Engineers are encouraged to work on \
cross-team projects and to approach problems from first principles. The co-founders remain \
actively involved in technical decisions. Stripe has maintained a private valuation exceeding \
$50 billion and is widely regarded as one of the most influential fintech companies globally, \
with a stated mission to increase the GDP of the internet.
"""


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


def embed_hardcoded_data() -> None:
    """Chunk and upsert the hardcoded Stripe data into ChromaDB.

    Uses upsert so this is safe to call on every import without creating
    duplicate documents.
    """
    collection = get_collection()
    chunks = chunk_text(STRIPE_DATA)
    ids = [f"stripe_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {"source": "hardcoded", "company": "Stripe", "chunk_index": i}
        for i in range(len(chunks))
    ]
    collection.upsert(documents=chunks, metadatas=metadatas, ids=ids)


def add_documents(texts: list[str], metadatas: list[dict]) -> None:
    collection = get_collection()
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(documents=texts, metadatas=metadatas, ids=ids)


# Embed hardcoded data on module load
embed_hardcoded_data()
