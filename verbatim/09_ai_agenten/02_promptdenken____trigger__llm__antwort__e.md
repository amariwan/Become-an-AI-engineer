# 09 ai agenten – Block 2

## Beschreibung

Prompt-Denken setzt auf Kontrolle im Moment: präzise formulieren für das beste Ergebnis in einem Schritt. Jede neue Situation erfordert neue Aufmerksamkeit, neuen Kontext, neue Entscheidung.
Loops verschieben das Modell. Statt jede Entscheidung selbst zu treffen, definierst du einen Rahmen, in dem Entscheidungen automatisch entstehen. Du steuerst nicht den Output. Du steuerst das System, das den Output erzeugt.

## Verbatim

```
   Prompt-Denken:    [Trigger] --> [LLM] --> [Antwort] --> Ende

   Loop-Denken:      [Trigger] --> [Plan] --> [Act] --> [Evaluate]
                                         ^                  |
                                         |   wiederholen    |
                                         +------------------+
                                                             |
                                         +--> [Finales Ergebnis]
```
