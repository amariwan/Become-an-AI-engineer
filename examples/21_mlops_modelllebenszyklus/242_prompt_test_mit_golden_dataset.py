# Prompt-Test mit Golden Dataset
# Quelle: chapters/21_mlops_modelllebenszyklus.tex (Zeile 242)
import pytest
from jinja2 import Template

GOLDEN = [
    {"input": "Wie kuendige ich mein Abo?",
     "expected_keywords": ["kuendigen", "Abo", "Optionen"]},
    {"input": "Ich habe meine Rechnung nicht erhalten",
     "expected_keywords": ["Rechnung", "erneut", "Support"]},
]

def test_prompt_golden():
    template = Template(open("prompts/support.jinja2").read())
    for case in GOLDEN:
        result = template.render(query=case["input"])
        for kw in case["expected_keywords"]:
            assert kw in result, \
                f"Fehlendes Schluesselwort {kw} in Prompt-Output"

