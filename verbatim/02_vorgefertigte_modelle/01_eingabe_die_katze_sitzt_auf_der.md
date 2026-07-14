# 02 vorgefertigte modelle – Block 1

## Beschreibung

\subsection{Pre-Training und Foundation Models}
Ein Foundation Model ist ein neuronales Netzwerk, das auf einem breiten Datensatz (oft mehrere Terabyte Text) mit einem selbstüberwachten Lernverfahren trainiert wurde. Das häufigste Verfahren ist die \textbf{Next-Token-Prediction}: Das Modell lernt, das nächste Wort in einer Sequenz vorherzusagen.

## Verbatim

```
  Eingabe: "Die Katze sitzt auf der"
  Ziel:     "Matte"
  Training: Modell sagt "Matte" vorher -> Fehler berechnen -> Gewichte anpassen
```
