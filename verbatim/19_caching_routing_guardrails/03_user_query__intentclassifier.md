# 19 caching routing guardrails – Block 3

## Beschreibung

\section{Semantic Router}
Ein Semantic Router klassifiziert jede Anfrage nach Intent und routed sie an das optimale Modell oder die optimale Pipeline:

## Verbatim

```
   [User Query] --> [Intent-Classifier]
                         |
          +--------------+--------------+
          |              |              |
     [Simple Q]    [Complex Q]    [Code Q]
          |              |              |
     [GPT-4o-mini]  [Claude Opus]  [Codestral]
          |              |              |
          +------+-------+------+------+
                 |              |
           [Cache Check]  [Refusal Check]
                 |              |
            [Response]     [Fallback]
```
