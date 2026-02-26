# from backend.rag.embeddings import get_collection
# collection = get_collection()
# print(collection.count())



# from backend.rag.embeddings import get_collection
# results = get_collection().query(query_texts=["What does Stripe do?"], n_results=3)
# print(results['documents'])



# from backend.rag.retriever import retrieve_context
# context = retrieve_context("What does Stripe do?")
# print(f"Found {len(context)} chunks")
# print(context[0][:200])




# from backend.rag.retriever import retrieve_context
# from backend.chains.report_chain import answer_query
# query = "What does Stripe do?"
# context = retrieve_context(query)
# print(f"Retrieved {len(context)} chunks")
# answer = answer_query(query, context)
# print(f"\nQ: {query}")
# print(f"A: {answer}")



# from backend.search.duckduckgo_client import search_web
# results = search_web("Stripe news", 5)
# print(len(results), results[0]['title'])



# from backend.search.duckduckgo_client import search_company
# all_results = search_company("Stripe")
# print(f"Total results: {len(all_results)}")
# print(f"Total results: {all_results}")



# from backend.search.duckduckgo_client import search_company, process_results
# raw = search_company("OpenAI")
# chunks = process_results(raw)
# print(f"Raw: {len(raw)} results -> {len(chunks)} unique chunks\n")
# for i, chunk in enumerate(chunks, 1):
#     print(f"{i}. {chunk[:120]}")




# import requests

# BASE = "http://localhost:8000"

# # Happy-path tests
# for company, query in [
#     ("OpenAI", "What does OpenAI do?"),
#     ("Airbnb", "What is Airbnb's tech stack?"),
# ]:
#     print(f"\n--- {company} ---")
#     resp = requests.post(f"{BASE}/research", json={"company_name": company, "query": query})
#     if resp.ok:
#         data = resp.json()
#         print(f"Status         : {data['status']}")
#         print(f"Sources found  : {data['sources_found']}")
#         print(f"Chunks embedded: {data['chunks_embedded']}")
#         print(f"Q: {data['query']}")
#         print(f"A: {data['answer'][:400]}")
#     else:
#         print(f"ERROR {resp.status_code}: {resp.text}")

# Error-case test: fake company should return 404
# print("\n--- XYZ123FAKE (expect 404) ---")
# resp = requests.post(f"{BASE}/research", json={"company_name": "XYZ123FAKE", "query": "What does XYZ123FAKE do?"})
# print(f"Status code: {resp.status_code}")
# print(f"Detail     : {resp.json().get('detail', resp.text)}")


# resp = requests.post(f"{BASE}/research", json={"company_name": "sfshffdsdfjjk3453", "query": "What does sfshffdsdfjjk3453 do?"})
# print(f"Status code: {resp.status_code}")
# print(f"Detail     : {resp.json().get('detail', resp.text)}")




# Phase 3

# from backend.agents.research_graph import ResearchState
# state = ResearchState(company_name="Claude", news_results=[], culture_results=[], tech_results=[], interview_results=[], all_results=[])
# print(state['company_name'])


# from backend.agents.research_graph import news_node
# state = {"company_name": "Tesla", "news_results": []}
# new_state = news_node(state)
# print(len(new_state['news_results']))
# print(new_state['news_results'])


# from backend.agents.research_graph import aggregator_node
# state = {"news_results": [{"title": "a"}], "culture_results": [{"title": "b"}], "tech_results": [], "interview_results": [], "all_results": []}
# new_state = aggregator_node(state)
# print(len(new_state['all_results']))

# from backend.agents.research_graph import build_graph
# app = build_graph()
# result = app.invoke({"company_name": "Tesla", "news_results": [], "culture_results": [], "tech_results": [], "interview_results": [], "all_results": []})
# print(len(result['all_results']))


