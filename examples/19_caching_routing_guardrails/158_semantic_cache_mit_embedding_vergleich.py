# Semantic Cache mit Embedding-Vergleich
# Quelle: chapters/19_caching_routing_guardrails.tex (Zeile 158)
import numpy as np
from openai import OpenAI

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.92):
        self.threshold = similarity_threshold
        self.embeddings: list[np.ndarray] = []
        self.responses: list[str] = []
        self.queries: list[str] = []
        self.client = OpenAI()

    def _embed(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return np.array(response.data[0].embedding)

    def _cosine_similarity(self, a: np.ndarray,
                           b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def lookup(self, query: str) -> tuple[str | None, float]:
        query_emb = self._embed(query)

        best_score = 0.0
        best_idx = -1

        for idx, stored_emb in enumerate(self.embeddings):
            score = self._cosine_similarity(query_emb, stored_emb)
            if score > best_score:
                best_score = score
                best_idx = idx

        if best_score >= self.threshold and best_idx >= 0:
            return self.responses[best_idx], best_score
        return None, best_score

    def store(self, query: str, response: str):
        emb = self._embed(query)
        self.embeddings.append(emb)
        self.responses.append(response)
        self.queries.append(query)

    def get_or_generate(self, query: str,
                        llm_func) -> tuple[str, bool]:
        cached, score = self.lookup(query)
        if cached:
            return cached, True
        response = llm_func(query)
        self.store(query, response)
        return response, False

# Nutzung
cache = SemanticCache(threshold=0.92)

def answer(query):
    response, is_cached = cache.get_or_generate(
        query, lambda q: call_llm(q)
    )
    status = "(CACHED)" if is_cached else "(GENERATED)"
    print(f"{status} Score: {cache.lookup(query)[1]:.2f}")
    return response

