# 03 modell landschaft – Block 5

## Beschreibung

\subsection{MoE -- Mixture of Experts}
Ein Architektur-Muster, bei dem das Modell aus vielen \glqq Experten\grqq{} (Sub-Netzwerken) besteht. Für jede Anfrage werden nur die relevanten Experten aktiviert, nicht das gesamte Netzwerk. Das Ergebnis: Die Leistung eines großen Modells bei den Kosten eines kleineren.

## Verbatim

```
  Ohne MoE:        Mit MoE:
  [LLM]            [Router] --+-- [Expert A] (Mathe)
                   (Anfrage)  +-- [Expert B] (Code)
                               +-- [Expert C] (Text)
                               +-- [Expert D] (Bild)

  Jede Anfrage:    Jede Anfrage:
  Alle 70B aktiv   Nur 7B von 70B aktiv
  -> hohe Kosten   -> niedrige Kosten
```
