# RAG mit pgvector und SQLAlchemy
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 406)
import os
from sqlalchemy import create_engine, text
from pgvector.sqlalchemy import Vector

class PgVectorStore:
    def __init__(self, connection_string: str = None):
        self.engine = create_engine(
            connection_string or os.environ["DATABASE_URL"]
        )
        self._init_vector_extension()

    def _init_vector_extension(self):
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    metadata JSONB,
                    embedding vector(1536)
                )
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_embedding
                ON document_chunks
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 200);
            """))
            conn.commit()

    def insert(self, content: str, embedding: list[float],
               metadata: dict = None):
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO document_chunks
                    (content, embedding, metadata)
                    VALUES (:content, :embedding, :metadata)
                """),
                {
                    "content": content,
                    "embedding": embedding,
                    "metadata": metadata or {},
                }
            )
            conn.commit()

    def search(self, query_embedding: list[float],
               top_k: int = 5) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT content, metadata,
                           1 - (embedding <=> :query) AS similarity
                    FROM document_chunks
                    ORDER BY embedding <=> :query
                    LIMIT :top_k
                """),
                {"query": query_embedding, "top_k": top_k}
            )
            return [
                {
                    "content": row[0],
                    "metadata": row[1],
                    "similarity": row[2],
                }
                for row in result
            ]

