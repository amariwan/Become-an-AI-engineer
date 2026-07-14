# 09 ai agenten – Block 1

## Beschreibung

Ein AI Agent nutzt LLMs als \textbf{Reasoning Engine}, um autonom Aufgaben zu planen und auszuführen. Der Agent entscheidet selbst, welche Tools in welcher Reihenfolge aufgerufen werden, bewertet Zwischenergebnisse und passt seine Strategie an.
AI Agents sind der dominierende Trend in der LLM-Entwicklung. Reine RAG-Systeme waren der vorherige Standard; Produktionsteams setzen jetzt auf agentische Systeme, die Recherche, Analyse, Entscheidung und Aktion in einem automatisierten Workflow vereinen.

## Verbatim

```
   Prompt:        [User] --> [LLM] --> [Antwort]

   RAG:           [User] --> [Retriever] --> [LLM] --> [Antwort mit Kontext]

   Agent:         [User] --> [LLM plant] --> [Tool 1] --> [LLM bewertet]
                               |                            |
                               +------- [Tool 2] <----------+
                                            |
                               +------- [Tool 3] <----------+
                               |                            |
                               +--> [Finale Antwort] <------+
```
