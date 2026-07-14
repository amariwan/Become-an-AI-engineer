# HyDE -- bessere Retrieval-Qualität
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 486)
def hyde_retrieval(query: str, retriever, llm) -> list[str]:
    """Generiert eine hypothetische Antwort und nutzt sie als Query."""

    # Schritt 1: Hypothetische Antwort generieren
    hyde_response = llm.invoke(
        f"Beantworte die folgende Frage knapp: {query}"
    )

    # Schritt 2: Die Antwort embedden (statt der Query)
    hyde_embedding = embedding_service.embed([hyde_response])[0]

    # Schritt 3: Mit dem Embedding suchen
    results = vector_db.search(hyde_embedding, top_k=5)
    return [r["content"] for r in results]

