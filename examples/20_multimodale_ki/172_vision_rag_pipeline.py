# Vision-RAG-Pipeline
# Quelle: chapters/20_multimodale_ki.tex (Zeile 172)
from openai import OpenAI


class VisionRAG:
    """RAG-Pipeline fuer bildbasierte Dokumente."""

    def __init__(self, vision_model: str = "gpt-4o",
                 embed_model: str = "text-embedding-3-large"):
        self.vision = MultimodalPipeline(model=vision_model)
        self.embed_client = OpenAI()
        self.embed_model = embed_model
        self.vector_store = {}

    def index_document(self, doc_id: str, image_paths: list[str]):
        """Dokument aus Bildern indexieren."""
        chunks = []
        for i, img_path in enumerate(image_paths):
            # Bild in Markdown uebersetzen
            description = self.vision.analyze_image(
                img_path,
                "Extrahiere den gesamten Text und beschreibe "
                "alle Diagramme, Tabellen und Abbildungen "
                "detailliert. Gib das Ergebnis als Markdown aus."
            )
            # Chunken
            for j, chunk in enumerate(self._chunk_text(description)):
                embedding = self.embed_client.embeddings.create(
                    model=self.embed_model,
                    input=chunk,
                ).data[0].embedding

                chunk_id = f"{doc_id}_p{i}_c{j}"
                self.vector_store[chunk_id] = {
                    "text": chunk,
                    "embedding": embedding,
                    "source": img_path,
                    "page": i,
                }
                chunks.append(chunk_id)

        return chunks

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_emb = self.embed_client.embeddings.create(
            model=self.embed_model, input=query
        ).data[0].embedding

        scores = [
            (cid, self._cosine_sim(query_emb, data["embedding"]))
            for cid, data in self.vector_store.items()
        ]
        scores.sort(key=lambda x: -x[1])

        return [
            {"chunk_id": cid, "score": score, **self.vector_store[cid]}
            for cid, score in scores[:top_k]
        ]

    def _chunk_text(self, text: str, size: int = 512) -> list[str]:
        words = text.split()
        return [" ".join(words[i:i+size])
                for i in range(0, len(words), size)]

    def _cosine_sim(self, a: list[float], b: list[float]) -> float:
        import numpy as np
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

