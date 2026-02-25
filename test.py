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

