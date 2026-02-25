from ddgs import DDGS
from ddgs.exceptions import DDGSException


def search_web(query: str, max_results: int = 10) -> list[dict]:
    """
    Search the web using DuckDuckGo.

    Returns a list of dicts with keys: title, snippet, url.
    Returns an empty list on any error.
    """
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", ""),
                })
    except DDGSException as e:
        print(f"[duckduckgo_client] Search error for '{query}': {e}")
    except Exception as e:
        print(f"[duckduckgo_client] Unexpected error for '{query}': {e}")
    return results


def search_news(company: str) -> list[dict]:
    return search_web(f"{company} latest news 2026", max_results=5)


def search_culture(company: str) -> list[dict]:
    return search_web(f"{company} company culture values employees", max_results=5)


def search_tech(company: str) -> list[dict]:
    return search_web(f"{company} tech stack engineering technology", max_results=5)


def search_interviews(company: str) -> list[dict]:
    return search_web(f"{company} interview process tips questions", max_results=5)


def process_results(results: list[dict]) -> list[str]:
    """
    Deduplicate by URL, clean whitespace, and combine title + snippet into text chunks.

    Returns a list of strings ready for embedding.
    """
    seen_urls = set()
    chunks = []
    for r in results:
        url = r.get("url", "").strip()
        if url in seen_urls:
            continue
        seen_urls.add(url)
        title = r.get("title", "").strip()
        snippet = r.get("snippet", "").strip()
        text = f"{title}. {snippet}".strip()
        if text and text != ".":
            chunks.append(text)
    return chunks


def search_company(company_name: str) -> list[dict]:
    """
    Run all 4 research queries for a company and return combined results.

    Returns up to 20 results covering news, culture, tech, and interviews.
    """
    results = []
    results.extend(search_news(company_name))
    results.extend(search_culture(company_name))
    results.extend(search_tech(company_name))
    results.extend(search_interviews(company_name))
    return results


if __name__ == "__main__":
    hits = search_company("Stripe")
    print(f"Got {len(hits)} total results:\n")
    for i, h in enumerate(hits, 1):
        print(f"{i}. {h['title']}")
        print(f"   {h['url']}")
        print(f"   {h['snippet'][:120]}...")
        print()
