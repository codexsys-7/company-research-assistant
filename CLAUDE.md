# Company Research Assistant - Development Guide

## Project Overview

AI-powered pre-interview research tool. Takes company name → autonomously researches web sources → generates structured briefing report → allows follow-up RAG chat.

**Goal:** Portfolio project demonstrating LLM/RAG/Agent skills for recruiters.

## Tech Stack

<!-- Phase 1 note: Originally planned Gemini 1.5 Flash, switched to OpenAI gpt-4o-mini due to Google Cloud quota issues (limit: 0 on GenerateContent). -->

- **LLM:** OpenAI gpt-4o-mini (switched from Gemini - see note above)
- **Agent Framework:** LangGraph
- **Vector Store:** ChromaDB (local, free)
- **Web Search:** DuckDuckGo (no API key needed)
- **Embeddings:** Sentence Transformers (local, free)
- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite + Tailwind
- **Containerization:** Docker Compose

## Environment Variables

```
OPENAI_API_KEY=<.env>
CHROMA_PERSIST_DIR=./chroma_db
BACKEND_PORT=8000
HF_TOKEN=<.env>
```

## Project Structure

```
company-research-assistant/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── rag/
│   │   ├── embeddings.py       # ChromaDB + embeddings
│   │   └── retriever.py        # RAG retrieval logic
│   ├── chains/
│   │   └── report_chain.py     # Report generation
│   ├── agents/
│   │   └── research_graph.py   # LangGraph agent (Phase 3)
│   ├── search/
│   │   └── duckduckgo_client.py # Web search (Phase 2)
│   ├── schemas/
│   │   └── report.py           # Pydantic models (Phase 4)
│   ├── requirements.txt
│   └── .env
├── frontend/                   # (Phase 5)
├── docker-compose.yml          # (Phase 6)
└── README.md                   # (Phase 7)
```

<!-- ## Hardcoded Data for Phase 1 Testing (COMPLETED - no longer needed)
Stripe is a financial infrastructure platform for businesses. Founded in 2010 by
Patrick and John Collison. Provides payment processing APIs for online businesses.
Serves millions of companies worldwide. Known for developer-friendly APIs and
excellent documentation. Valued at $50B+. Main products: Payments, Billing, Connect,
Terminal. Tech stack: Ruby, Scala, React, MongoDB. Strong engineering culture with
focus on developer experience.
-->

## Development Phases

<!-- **Phase 1:** Foundation & Basic RAG (Day 1) ✅ COMPLETED Feb 24, 2026
- FastAPI server + ChromaDB + Sentence Transformers
- Hardcoded Stripe data embedded
- RAG retrieval working with OpenAI gpt-4o-mini (switched from Gemini)
- POST /research endpoint tested via curl - all queries returning correct answers
-->

<!-- **Phase 2:** Live Web Search (Day 2) COMPLETED Feb 25, 2026
- DuckDuckGo integration (ddgs library, 4 query templates: news, culture, tech, interviews)
- process_results() deduplication + title+snippet cleaning
- embed_search_results() chunks at 250 words, upserts to ChromaDB with {company, source} metadata
- clear_collection() called before each research request to flush stale data
- /research endpoint: clear -> search_company -> process_results -> embed -> retrieve -> LLM -> JSON
- Returns: answer, company, query, sources_found, chunks_embedded
- Tested: OpenAI (20 sources, 20 chunks), Airbnb (20 sources, 20 chunks) - both returning live answers
-->

**Phase 3:** LangGraph Agents (Day 3)

- 4 parallel research nodes
- State management
- Agent graph execution

**Phase 4:** Structured Reports (Day 4)

- Pydantic report schema
- /generate-report endpoint
- /chat endpoint for follow-ups

**Phase 5:** React Frontend (Day 5)

- SearchBar, ReportView, ChatInterface components
- Full UI flow

**Phase 6:** Docker + Testing (Day 6)

- Docker Compose setup
- End-to-end testing
- Bug fixes

**Phase 7:** Documentation (Day 7)

- Professional README
- Demo GIF
- GitHub push

## ✅ Completed Phases

**Phase 1:** Foundation & Basic RAG — COMPLETED Feb 24, 2026

**Phase 2:** Live Web Search (Day 2) COMPLETED Feb 25, 2026

## 🔄 Current Phase

**Phase 3:** LangGraph Agents (Feb 26, 2026)

**Next immediate steps:**

- Create `backend/agents/research_graph.py`
- 4 parallel research nodes (news, culture, tech, interviews)
- State management with LangGraph
- Agent graph execution wired into `/research` endpoint
