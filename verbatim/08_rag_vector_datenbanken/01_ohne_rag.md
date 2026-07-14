# 08 rag vector datenbanken – Block 1

## Beschreibung

(keine direkte Beschreibung)

## Verbatim

```
   Ohne RAG:
   [User-Frage] --> [LLM] --> [Antwort (nur aus Training)]

   Mit RAG:
   [User-Frage] --> [Retriever] --> [Vector DB]
                       |                |
                       v                v
   [Retrieved Docs] + [User-Frage] --> [LLM] --> [Faktenbasierte Antwort]
```
