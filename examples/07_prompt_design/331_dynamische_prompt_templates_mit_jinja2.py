# Dynamische Prompt-Templates mit Jinja2
# Quelle: chapters/07_prompt_design.tex (Zeile 331)
from jinja2 import Template

PROMPT_TEMPLATE = Template("""
Du klassifizierst Support-Tickets. JSON-Output: priority, category, urgency.

{% for ex in examples %}
Input: {{ ex.input }}
Output: {{ ex.output }}
{% endfor %}

Ticket:
Kunde: {{ customer_name }}
Text: {{ ticket_text }}
Antworten: nur JSON.
""")

prompt = PROMPT_TEMPLATE.render(
    examples=few_shot_examples,
    customer_name="Meyer",
    ticket_text="Abo-Kuendigung nicht bearbeitet!",
)

