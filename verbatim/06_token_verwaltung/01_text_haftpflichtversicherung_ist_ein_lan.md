# 06 token verwaltung – Block 1

## Beschreibung

Ein 500-Wort-englischer Text wird typischerweise zu \textbf{\~650 Tokens}, der gleiche deutsche Text zu \textbf{\~850--1.000 Tokens}. Das bedeutet 30--50\,\% höhere Kosten für deutsche Texte bei gleichem Inhalt.
\subsection{Tokenisierung visualisieren}

## Verbatim

```
Text: "Haftpflichtversicherung ist ein langes Wort."

GPT-4o (tiktoken):
  [Haf] [t] [pfl] [icht] [vers] [ich] [er] [ung] [ist] [ein] [lang] [es] [Wort] [.]
  = 14 Tokens

Claude (SentencePiece):
  [_Haft] [pfl] [icht] [vers] [icher] [ung] [_ist] [_ein] [_langes] [_Wort] [.]
  = 11 Tokens (effizienter bei Komposita)
```
