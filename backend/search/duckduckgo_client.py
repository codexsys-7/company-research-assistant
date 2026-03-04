import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

_client = TavilyClient(api_key=os.getenv("TAVILY"))


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web using Tavily.
    Returns a list of dicts with keys: title, snippet, url.
    Returns an empty list on any error.
    """
    try:
        response = _client.search(query, max_results=max_results)
        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "snippet": r.get("content", ""),
                "url": r.get("url", ""),
            })
        return results
    except Exception as e:
        print(f"[search_web] Error for '{query}': {e}")
        return []


def search_news(company: str) -> list[dict]:
    return search_web(f"{company} latest news", max_results=5)


def search_culture(company: str) -> list[dict]:
    return search_web(f"{company} company culture values employees", max_results=5)


def search_tech(company: str) -> list[dict]:
    return search_web(f"{company} tech stack engineering technology", max_results=5)


def search_financials(company: str) -> list[dict]:
    revenue = search_web(f"{company} annual revenue earnings financial results", max_results=3)
    valuation = search_web(f"{company} market cap valuation stock price funding", max_results=3)
    return revenue + valuation


def search_interviews(company: str) -> list[dict]:
    glassdoor = search_web(f"{company} interview questions Glassdoor candidate experience", max_results=3)
    leetcode = search_web(f"site:leetcode.com {company} interview questions experience", max_results=3)
    return glassdoor + leetcode


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
    """Run all research queries for a company and return combined results."""
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
