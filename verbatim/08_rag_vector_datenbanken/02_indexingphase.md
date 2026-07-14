# 08 rag vector datenbanken – Block 2

## Beschreibung

(keine direkte Beschreibung)

## Verbatim

```
   Indexing-Phase:
   [PDF] -> [Chunker] -> [Chunks] -> [Embedding] -> [Vector DB]
                                         |
                                   text-embedding-3-small

   Runtime-Phase:
   [Query] -> [Embedding] -> [Vector DB (ANN Search)] -> [Top-K Chunks]
                                                              |
                                                              v
   [System-Prompt] + [Chunks] + [Query] -> [LLM] -> [Antwort]
```
