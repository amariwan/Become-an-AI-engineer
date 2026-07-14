# RAG-Schutz: Retrieval-Ergebnisse nach Vertrauenswürdigkeit filtern
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 623)
GOLDEN_DATASET_TRUST = 0.9
USER_UPLOAD_TRUST = 0.3

def safe_retrieve(vector_store, query: str, top_k: int = 5) -> list[dict]:
    results = vector_store.similarity_search_with_score(query, k=top_k * 3)

    weighted_results = []
    for doc, score in results:
        trust = doc.metadata.get("trust_score", 0.5)
        weighted_results.append({
            "doc": doc,
            "similarity": score,
            "trust": trust,
            "combined": score * trust,
        })

    weighted_results.sort(key=lambda x: x["combined"], reverse=True)
    trusted = [r for r in weighted_results if r["trust"] >= 0.7]
    if trusted:
        return [r["doc"] for r in trusted[:top_k]]

    print("WARNUNG: Keine ausreichend vertrauenswuerdigen Dokumente gefunden")
    return [r["doc"] for r in weighted_results[:top_k] if r["trust"] >= 0.5]

