# 07 prompt design – Block 3

## Beschreibung

\section{Architektur -- Prompt-Pipelines in Produktion}
In Produktion sind Prompts selten eine einzelne Nachricht. Sie durchlaufen eine Pipeline:

## Verbatim

```
   Input-Daten
      |
      v
   [Pre-Processing]   --> Datenbereinigung, Formatierung, Kontext-Anreicherung
      |
      v
   [Template-Rendering] --> Jinja2-Engine befuellt Prompt-Template
      |
      v
   [Token-Budget-Check] --> Input-Tokens zaehlen, ggf. truncaten
      |
      v
   [API-Call]         --> OpenAI / Anthropic / Google
      |
      v
   [Post-Processing]  --> JSON parsen, validieren, transformieren
      |
      v
   [Output]           --> strukturiertes Ergebnis
```
