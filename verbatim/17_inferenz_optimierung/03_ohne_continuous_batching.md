# 17 inferenz optimierung – Block 3

## Beschreibung

\subsection{Continuous Batching}
Ohne Batching wird jeder Request einzeln verarbeitet -- eine GPU ist zu 100\,\% ausgelastet, aber nur für einen Request. Continuous Batching (auch \textit{dynamisches Batching}) erlaubt es, neue Requests in einen laufenden Batch aufzunehmen, sobald ein vorheriger Request abgeschlossen ist:

## Verbatim

```
   Ohne Continuous Batching:
   [Req 1] [______][Req 2][______][Req 3][______]
   GPU-Auslastung: ~50%

   Mit Continuous Batching:
   [Req 1] [Req 2] [Req 3] [Req 4] [Req 5] [Req 6]
   GPU-Auslastung: ~95%
```
