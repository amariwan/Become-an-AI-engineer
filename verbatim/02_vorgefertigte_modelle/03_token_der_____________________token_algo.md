# 02 vorgefertigte modelle – Block 3

## Beschreibung

MoE-Modelle bestehen aus vielen spezialisierten Sub-Netzwerken (Experts)
und einem Router, der für jeden Token nur einen Bruchteil der Experten
aktiviert. Dadurch erreichen sie die Kapazität großer Modelle bei den
Kosten kleinerer.

## Verbatim

```
Token "der"                     Token "Algorithmus"
            |                               |
    +-------v--------+            +----------v----------+
    |    Router      |            |       Router        |
    +----+----+-----+            +-----+----+----+-----+
         |    |                          |    |    |
    [Expert A] [Expert C]          [Expert B] [Expert D]
    (Grammatik) (Alltag)          (Fachtext) (Logik)
```
