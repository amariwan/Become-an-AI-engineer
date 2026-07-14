# 04 kontext preise – Block 2

## Beschreibung

\section{Architektur -- Context-Management in Produktion}
Jeder LLM-Call durchläuft ein Context-Budgeting:

## Verbatim

```
    Request kommt an
         |
         v
    [Context-Budget: max 100K Tokens]
         |
    +----+----+
    |         |
    RAG      Chat-History
    (50K)    (30K)
    |         |
    +----+----+
         |
    System-Prompt (5K)
         |
    User-Input (1K)
         |
    Summe: 86K < 100K => OK
```
