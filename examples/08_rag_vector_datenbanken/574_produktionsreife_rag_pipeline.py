# Produktionsreife RAG-Pipeline
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 574)
import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RAGConfig:
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 5
    rerank: bool = False
    hyde: bool = False

class RAGPipeline:
    def __init__(self, config: RAGConfig):
        self.config = config
        self.embedder = EmbeddingService(provider="openai")
        self.vector_store = self._init_vector_store()
        self.llm = openai_client

    def _init_vector_store(self):
        return Chroma(
            collection_name="rag_knowledge_base",
            embedding_function=OpenAIEmbeddings(
                model=self.config.embedding_model
            ),
            persist_directory="./chroma_db",
        )

    def add_documents(self, documents: list[str],
                      metadata: Optional[list[dict]] = None):
        chunks = ChunkingStrategy.recursive(
            documents,
            chunk_size=self.config.chunk_size,
            overlap=self.config.chunk_overlap,
        )
        metadatas = metadata or [{}] * len(chunks)
        self.vector_store.add_documents(chunks, metadatas=metadatas)

    def query(self, question: str) -> dict:
        if self.config.hyde:
            hyde_response = self.llm.invoke(
                f"Beantworte knapp: {question}"
            )
            query_text = hyde_response
        else:
            query_text = question

        docs = self.vector_store.similarity_search(
            query_text,
            k=self.config.top_k,
        )

        if self.config.rerank:
            docs = self._rerank(question, docs)

        context = "\n\n---\n\n".join(d.page_content for d in docs)
        response = self.llm.chat.completions.create(
            model=self.config.llm_model,
            messages=[{
                "role": "system",
                "content": (
                    "Du beantwortest Fragen basierend auf dem Kontext. "
                    "Wenn der Kontext nicht ausreicht: 'Nicht genug Daten.' "
                    "Zitiere Quellen aus dem Kontext."
                )
            }, {
                "role": "user",
                "content": f"Kontext:\n{context}\n\nFrage:\n{question}",
            }],
            temperature=0.1,
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": [
                {"content": d.page_content, "score": d.metadata.get("score")}
                for d in docs
            ],
            "usage": response.usage,
        }

