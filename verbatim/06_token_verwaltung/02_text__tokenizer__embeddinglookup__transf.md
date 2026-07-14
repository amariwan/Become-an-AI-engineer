# 06 token verwaltung – Block 2

## Beschreibung

\section{Architektur -- Wie Tokens durch die Pipeline fließen}
Token-Management ist kein isolierter Schritt, sondern durchzieht die gesamte LLM-Pipeline:

## Verbatim

```
  Text -> Tokenizer -> Embedding-Lookup -> Transformer -> Output-Logits -> Detokenizer -> Text

  Kosten-Falle #1:        Kosten-Falle #2:         Kosten-Falle #3:
  Unnötig lange Prompts   Kein max_tokens          Chat-History wächst unbegrenzt
```
