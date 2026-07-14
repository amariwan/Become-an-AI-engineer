# 09 ai agenten – Block 7

## Beschreibung

\subsection{Augmented LLMs}
Der Grundgedanke: Ein LLM allein kann keine externen Aktionen ausführen. Es ist ein reiner Textgenerator. Durch die Kopplung mit Tools (\textbf{Augmented LLM}) wird es handlungsfähig:

## Verbatim

```
   Basismodell:    Text-in -> Text-out

   Augmented LLM:  Text-in -> Tool-Decision -> Tool-Result -> Text-out

   Der entscheidende Unterschied:
   Das LLM gibt nicht nur Text aus, sondern auch die Entscheidung,
   welches Tool aufgerufen werden soll.
```
