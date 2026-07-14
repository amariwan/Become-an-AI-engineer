# 04 kontext preise – Block 4

## Beschreibung

\subsection{Cache-Effekte nutzen}
Wenn dein System-Prompt konstant bleibt (z.B. 5K Tokens), kannst du
durch Prompt-Caching 50--90\,\% der Input-Kosten sparen:

## Verbatim

```
    Ohne Caching:   10.000 Queries * 10K Input = 100 Mio Tokens/Tag
    Mit Caching:    10.000 Queries * 5K (dynamisch) + 5K (1x gecached)
                    = 50 Mio Tokens/Tag + 5K einmalig
    Ersparnis:      ~50% bei Input-Kosten
```
