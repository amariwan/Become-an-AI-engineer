# 17 inferenz optimierung – Block 1

## Beschreibung

(keine direkte Beschreibung)

## Verbatim

```
   Prefill-Phase (parallel):
   [Token 1] [Token 2] [Token 3] ... [Token N]
      |          |          |             |
      +----------+----------+-----+-------+
                                   |
                              [KV-Cache]
                                   |
                              [Token N+1]

   Decode-Phase (sequentiell):
   [Token N+1] --> [KV-Cache] --> [Token N+2] --> [KV-Cache] --> ...
```
