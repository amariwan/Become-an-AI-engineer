# 19 caching routing guardrails – Block 2

## Beschreibung

Der mächtigste -- und komplexeste -- Cache-Ansatz: Ähnliche Anfragen erkennen und die zwischengespeicherte Antwort einer semantisch äquivalenten Frage zurückgeben.
\subsection{Architektur}

## Verbatim

```
   [User Query] --> [Embedding-Modell] --> [Vector Search]
                                              |
                                   +----------+----------+
                                   |                     |
                              [Hit > Threshold]    [Miss < Threshold]
                                   |                     |
                              [Cache Response]    [LLM Call]
                                                      |
                                              [Store in Cache]
```
