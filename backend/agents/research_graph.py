import time
import logging
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
try:
    from search.duckduckgo_client import search_news, search_culture, search_tech, search_interviews, process_results
except ModuleNotFoundError:
    from backend.search.duckduckgo_client import search_news, search_culture, search_tech, search_interviews, process_results

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    company_name: str
    news_results: list
    culture_results: list
    tech_results: list
    interview_results: list
    all_results: list


def news_node(state: ResearchState) -> ResearchState:
    company = state["company_name"]
    print(f"[news_node] Searching news for: {company}")
    t0 = time.time()
    results = search_news(company)
    elapsed = round(time.time() - t0, 2)
    if not results:
        logger.warning("[news_node] No results returned for '%s' — continuing", company)
    print(f"[news_node] Found {len(results)} results in {elapsed}s")
    time.sleep(1)
    return {**state, "news_results": results}


def culture_node(state: ResearchState) -> ResearchState:
    company = state["company_name"]
    print(f"[culture_node] Searching culture for: {company}")
    t0 = time.time()
    results = search_culture(company)
    elapsed = round(time.time() - t0, 2)
    if not results:
        logger.warning("[culture_node] No results returned for '%s' — continuing", company)
    print(f"[culture_node] Found {len(results)} results in {elapsed}s")
    time.sleep(1)
    return {**state, "culture_results": results}


def tech_node(state: ResearchState) -> ResearchState:
    company = state["company_name"]
    print(f"[tech_node] Searching tech stack for: {company}")
    t0 = time.time()
    results = search_tech(company)
    elapsed = round(time.time() - t0, 2)
    if not results:
        logger.warning("[tech_node] No results returned for '%s' — continuing", company)
    print(f"[tech_node] Found {len(results)} results in {elapsed}s")
    time.sleep(1)
    return {**state, "tech_results": results}


def interview_node(state: ResearchState) -> ResearchState:
    company = state["company_name"]
    print(f"[interview_node] Searching interviews for: {company}")
    t0 = time.time()
    results = search_interviews(company)
    elapsed = round(time.time() - t0, 2)
    if not results:
        logger.warning("[interview_node] No results returned for '%s' — continuing", company)
    print(f"[interview_node] Found {len(results)} results in {elapsed}s")
    time.sleep(1)
    return {**state, "interview_results": results}


def aggregator_node(state: ResearchState) -> ResearchState:
    combined = (
        state["news_results"]
        + state["culture_results"]
        + state["tech_results"]
        + state["interview_results"]
    )
    print(f"[aggregator_node] Combining {len(combined)} total results")
    processed = process_results(combined)
    print(f"[aggregator_node] {len(processed)} unique chunks after processing")
    return {**state, "all_results": processed}


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("news", news_node)
    graph.add_node("culture", culture_node)
    graph.add_node("tech", tech_node)
    graph.add_node("interview", interview_node)
    graph.add_node("aggregator", aggregator_node)

    graph.add_edge(START, "news")
    graph.add_edge("news", "culture")
    graph.add_edge("culture", "tech")
    graph.add_edge("tech", "interview")
    graph.add_edge("interview", "aggregator")
    graph.add_edge("aggregator", END)

    app = graph.compile()
    return app

