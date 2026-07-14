# 19 caching routing guardrails – Block 4

## Beschreibung

\section{Guardrails -- Sicherheit für LLM-Systeme}
Guardrails sind Validierungsschichten vor und nach dem LLM-Call:

## Verbatim

```
   [User Input] --> [Input Guard] --> [LLM] --> [Output Guard] --> [User]
                        |                           |
                   [PII Redact]              [Content Filter]
                   [Injection Check]          [Schema Validate]
                   [Length Limit]             [Hallucination Check]
```
