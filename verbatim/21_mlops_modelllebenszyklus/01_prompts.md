# 21 mlops modelllebenszyklus – Block 1

## Beschreibung

\subsection{Strukturierte Prompt-Ordner}
Eine bewährte Struktur trennt Prompts nach Umgebung und Domäne:

## Verbatim

```
prompts/
  staging/
    customer-support/
      v1__de-escalation.jinja2
      v2__de-escalation.jinja2
    code-assistant/
      v3__code-review.jinja2
  production/
    customer-support/
      v2__de-escalation.jinja2
    code-assistant/
      v3__code-review.jinja2
```
