# 08 rag vector datenbanken – Block 4

## Beschreibung

\subsection{RAPTOR (Recursive Abstractive Processing)}
RAPTOR baut eine Hierarchie von Zusammenfassungen auf -- Textblöcke werden zusammengefasst, diese Zusammenfassungen wiederum. Das Retrieval sucht auf der passenden Hierarchie-Ebene:

## Verbatim

```
   Level 2: [Gesamt-Zusammenfassung]
                /        \
   Level 1: [Summary A]  [Summary B]  ...
               |            |
   Level 0: [Chunk 1-5]  [Chunk 6-10]  ...

   Vorteil: Uebergreifende Fragen werden auf Level 1/2 beantwortet,
   Detail-Fragen auf Level 0.
```
