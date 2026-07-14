# Batch-Indexing für bessere Performance
# Quelle: chapters/08_rag_vector_datenbanken.tex (Zeile 744)
def batch_index(documents: list[str],
                embedder, vector_store,
                batch_size: int = 100):

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        embeddings = embedder.embed(batch)
        vector_store.add_embeddings(batch, embeddings)
        print(f"Indexed {i + len(batch)} / {len(documents)} chunks")

