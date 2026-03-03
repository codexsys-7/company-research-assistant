import time
import logging
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
try:
    from search.duckduckgo_client import search_news, search_culture, search_tech, search_interviews, search_financials, process_results
    from chains.report_generator import generate_report
    from schemas.report import CompanyReport
except ModuleNotFoundError:
    from backend.search.duckduckgo_client import search_news, search_culture, search_tech, search_interviews, search_financials, process_results
    from backend.chains.report_generator import generate_report
    from backend.schemas.report import CompanyReport

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    company_name: str
    news_results: list
    culture_results: list
    tech_results: list
    interview_results: list
    financials_results: list
    all_results: list
    report: Optional[CompanyReport]


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


def financials_node(state: ResearchState) -> ResearchState:
    company = state["company_name"]
    print(f"[financials_node] Searching financials for: {company}")
    t0 = time.time()
    results = search_financials(company)
    elapsed = round(time.time() - t0, 2)
    if not results:
        logger.warning("[financials_node] No results returned for '%s' — continuing", company)
    print(f"[financials_node] Found {len(results)} results in {elapsed}s")
    time.sleep(1)
    return {**state, "financials_results": results}


def aggregator_node(state: ResearchState) -> ResearchState:
    combined = (
        state["news_results"]
        + state["culture_results"]
        + state["tech_results"]
        + state["interview_results"]
        + state["financials_results"]
    )
    print(f"[aggregator_node] Combining {len(combined)} total results")
    processed = process_results(combined)
    print(f"[aggregator_node] {len(processed)} unique chunks after processing")
    return {**state, "all_results": processed}


def report_generator_node(state: ResearchState) -> ResearchState:
    company = state["company_name"]
    print(f"[report_generator_node] Generating structured report for: {company}")
    t0 = time.time()
    report = generate_report(company, state["all_results"])
    elapsed = round(time.time() - t0, 2)
    print(f"[report_generator_node] Report generated in {elapsed}s")
    return {**state, "report": report}


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("news", news_node)
    graph.add_node("culture", culture_node)
    graph.add_node("tech", tech_node)
    graph.add_node("interview", interview_node)
    graph.add_node("financials", financials_node)
    graph.add_node("aggregator", aggregator_node)
    graph.add_node("report_generator", report_generator_node)

    graph.add_edge(START, "news")
    graph.add_edge("news", "culture")
    graph.add_edge("culture", "tech")
    graph.add_edge("tech", "interview")
    graph.add_edge("interview", "financials")
    graph.add_edge("financials", "aggregator")
    graph.add_edge("aggregator", "report_generator")
    graph.add_edge("report_generator", END)

    app = graph.compile()
    return app

