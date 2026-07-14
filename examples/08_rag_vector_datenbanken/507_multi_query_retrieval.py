# Multi-Query Retrieval
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 507)
def multi_query_retrieval(query: str, retriever, llm,
                          n_queries: int = 3) -> list[str]:
    queries = llm.invoke(
        f"Generiere {n_queries} verschiedene Formulierungen "
        f"dieser Frage, um alle relevanten Informationen zu finden:"
        f"\n{query}"
    )

    all_docs = []
    for q in queries:
        docs = retriever.get_relevant_documents(q)
        all_docs.extend(docs)

    # Deduplizieren
    seen = set()
    unique = []
    for d in all_docs:
        if d.page_content not in seen:
            seen.add(d.page_content)
            unique.append(d)
    return unique[:top_k]

