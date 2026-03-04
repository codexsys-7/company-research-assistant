# Company Research Assistant - Development Guide

## Project Overview

AI-powered pre-interview research tool. Takes company name → autonomously researches web sources → generates structured briefing report → allows follow-up RAG chat.

**Goal:** Portfolio project demonstrating LLM/RAG/Agent skills for recruiters.

**Status:** All 7 phases COMPLETE. Project is live and deployed.

---

## Tech Stack

- **LLM:** OpenAI gpt-4o-mini
- **Agent Framework:** LangGraph (sequential pipeline)
- **Vector Store:** ChromaDB (local)
- **Web Search:** Tavily API (`TAVILY` env var)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Backend:** FastAPI (Python 3.11+)
- **Frontend:** React 19 + Vite 7 + Tailwind CSS v3
- **Deployment:** Render (free tier)

> **Note:** Originally used Gemini (switched to OpenAI — quota issue), DuckDuckGo (switched to Tavily — reliability), and Sentence Transformers (switched to OpenAI embeddings — Render cold-start timeout).

---

## Environment Variables

```
OPENAI_API_KEY=sk-...        # LLM + embeddings
TAVILY=tvly-...              # Web search
CHROMA_PERSIST_DIR=./chroma_db
```

---

## Project Structure

```
company-research-assistant/
├── backend/
│   ├── main.py                     # FastAPI entry point (/research, /generate-report, /chat)
│   ├── agents/
│   │   └── research_graph.py       # LangGraph pipeline (6 search nodes + aggregator + report_generator)
│   ├── chains/
│   │   ├── report_generator.py     # LLM prompt + CompanyReport generation
│   │   └── report_chain.py         # RAG chain for /chat endpoint
│   ├── rag/
│   │   ├── embeddings.py           # ChromaDB helpers (get_collection, embed, clear)
│   │   └── retriever.py            # retrieve_context(query, k=3)
│   ├── schemas/
│   │   └── report.py               # CompanyReport Pydantic model (11 fields + validators)
│   ├── search/
│   │   └── duckduckgo_client.py    # Tavily search client (legacy name)
│   ├── requirements.txt
│   └── .env                        # (gitignored)
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Root component + LoadingScreen + app state
│   │   ├── api.js                  # Axios instance + generateReport() + chat()
│   │   └── components/
│   │       ├── SearchBar.jsx
│   │       ├── ReportView.jsx
│   │       └── ChatInterface.jsx
│   ├── public/favicon.svg
│   ├── .env                        # (gitignored) VITE_API_URL= for dev
│   ├── .env.example
│   ├── .env.production             # VITE_API_URL=https://your-backend.onrender.com
│   ├── tailwind.config.js
│   ├── vite.config.js              # Proxy: /api/* → localhost:8000
│   └── package.json
├── demo_files/
│   └── CRA_Demo.gif
├── render.yaml                     # Render deployment config (backend web service)
├── CLAUDE.md
└── README.md
```

---

## Key Architecture Notes

- **LangGraph pipeline:** `START → news → culture → tech → interview → financials → aggregator → report_generator → END`
  - All sequential — fan-out parallelism abandoned (Tavily client deadlocks in LangGraph thread executor)
  - Each node: 5 results; interview node: 6 (Glassdoor + LeetCode site:); financials node: 6 (revenue + valuation)
  - ~27 total sources per research session
- **ChromaDB is empty when `report_generator_node` runs** — embedding happens after `graph.invoke()` returns in `main.py`. `report_generator.py` uses `all_context` fallback.
- **Single ChromaDB collection** — cleared before each new research session via `clear_collection()`
- **Vite proxy** (dev only): `/api/*` → `localhost:8000` (strips `/api` prefix) — avoids CORS
- **CORS** (backend): allows `localhost:5173` + `*.onrender.com` regex

---

## CompanyReport Schema (11 fields)

`company_name`, `overview`, `products_and_services`, `tech_stack` (List), `culture_and_values`,
`recent_news` (List, max 5), `financials`, `interview_process`, `common_interview_questions` (List),
`red_flags` (List), `preparation_tips`

Validators: `filter_sentinel_strings` (tech_stack, red_flags, common_interview_questions),
`limit_and_filter_recent_news` (caps at 5, also filters sentinels)

---

## Live URLs

| Service  | URL |
|----------|-----|
| Frontend | https://company-research-assistant-frontend.onrender.com |
| Backend  | https://company-research-assistant-j8om.onrender.com |
| GitHub   | https://github.com/codexsys-7/company-research-assistant |

---

## ✅ All Phases Completed

| Phase | Description | Date |
|-------|-------------|------|
| 1 | Foundation & Basic RAG (FastAPI + ChromaDB + hardcoded data) | Feb 24, 2026 |
| 2 | Live Web Search (DuckDuckGo → later Tavily) | Feb 25, 2026 |
| 3 | LangGraph Agents (sequential multi-node pipeline) | Feb 26, 2026 |
| 4 | Structured Reports (CompanyReport schema + /generate-report + /chat) | Mar 2, 2026 |
| 5 | React Frontend (Vite + Tailwind + LoadingScreen + ChatInterface) | Mar 4, 2026 |
| 6 | Render Deployment (render.yaml + OpenAI embeddings + Tavily switch) | Mar 4, 2026 |
| 7 | Documentation (README + Demo GIF + GitHub push) | Mar 4, 2026 |
