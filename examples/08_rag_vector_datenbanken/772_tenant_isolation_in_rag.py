# Tenant-Isolation in RAG
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 772)
class TenantAwareRetriever:
    def __init__(self, vector_store, tenant_id: str):
        self.store = vector_store
        self.tenant_id = tenant_id

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        # Metadaten-Filter stellt sicher: nur Chunks dieses Tenants
        return self.store.similarity_search(
            query,
            k=top_k,
            filter={"tenant_id": self.tenant_id},
        )

    def add_document(self, content: str, embedding: list[float]):
        self.store.insert(
            content=content,
            embedding=embedding,
            metadata={"tenant_id": self.tenant_id},
        )

