# 03 modell landschaft – Block 3

## Beschreibung

(keine direkte Beschreibung)

## Verbatim

```
   Ohne MCP:        [LLM] --[Custom Code]--> [API A]
                      | --[Custom Code]--> [DB B]
                      | --[Custom Code]--> [Tool C]

   Mit MCP:          [LLM] --[MCP Client]--> [MCP Server] --> [API A]
                                               |           --> [DB B]
                                               |           --> [Tool C]
```
