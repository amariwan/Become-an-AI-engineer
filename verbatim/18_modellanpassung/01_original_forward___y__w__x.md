# 18 modellanpassung – Block 1

## Beschreibung

\subsection{Wie LoRA funktioniert}
LoRA fügt für jede trainierbare Schicht zwei kleine Matrizen $A$ und $B$ hinzu, deren Produkt $A \cdot B$ die Gewichtsänderung $\Delta W$ approximiert:

## Verbatim

```
   Original Forward:   y = W * x
   LoRA Forward:       y = W * x + (B * A) * x
                                \_______/
                            rang-reduziertes Update

   W:    Originalgewichte (eingefroren, nicht trainiert)
   A, B: LoRA-Matrizen (trainiert)
   Rang: Kontrolliert die Anzahl trainierbarer Parameter
```
