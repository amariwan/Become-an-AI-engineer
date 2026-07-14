# Re-Ranking verbessert Retrieval-Qualität
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 662)
class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: list[str],
               top_k: int = 3) -> list[tuple[str, float]]:
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        scored = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )
        return scored[:top_k]

