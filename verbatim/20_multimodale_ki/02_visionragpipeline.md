# 20 multimodale ki – Block 2

## Beschreibung

\subsection{Vision RAG -- Bilder durchsuchbar machen}
Ein Dokument mit Diagrammen, Screenshots und handschriftlichen Notizen kann nicht direkt in einer Vector-DB gespeichert werden. Die Lösung: \textbf{Vision RAG} -- Bilder werden durch ein multimodales Modell in Text-Beschreibungen übersetzt, die dann gechunkt und embedded werden.

## Verbatim

```
   Vision-RAG-Pipeline:

   [PDF-Seite] --> [Vision-LLM] --> [Markdown-Beschreibung]
                                        |
                                   [Chunk + Embed]
                                        |
                                   [Vector DB]
                                        |
   [Query] --> [Text-Embedding] --> [Retrieval] --> [LLM-Response]
```
