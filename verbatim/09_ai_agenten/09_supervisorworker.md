# 09 ai agenten – Block 9

## Beschreibung

\subsection{Architekturmuster}
Drei Muster haben sich in der Produktion bewährt:

## Verbatim

```
   Supervisor-Worker:
   [User] --> [Supervisor] --> [Worker A: Recherche]
                          --> [Worker B: Analyse]
                          --> [Worker C: Bericht]
                               |
                          [Supervisor aggregiert]
                               |
                          [Antwort an User]
```
