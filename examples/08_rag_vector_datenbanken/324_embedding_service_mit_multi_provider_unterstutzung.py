# Embedding-Service mit Multi-Provider-Unterstützung
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 324)
from openai import OpenAI
import numpy as np

class EmbeddingService:
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.client = OpenAI()

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self.provider == "openai":
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
            )
            return [r.embedding for r in response.data]

        elif self.provider == "cohere":
            import cohere
            co = cohere.Client()
            response = co.embed(
                texts=texts,
                model="embed-multilingual-v3.0",
                input_type="search_document",
            )
            return response.embeddings

        elif self.provider == "voyage":
            import voyageai
            vo = voyageai.Client()
            response = vo.embed(
                texts=texts,
                model="voyage-2",
                input_type="document",
            )
            return response.embeddings

    def similarity(self, a: list[float], b: list[float]) -> float:
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (
            np.linalg.norm(a_np) * np.linalg.norm(b_np)
        ))

