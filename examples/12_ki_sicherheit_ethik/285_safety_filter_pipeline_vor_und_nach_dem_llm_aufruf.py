# Safety-Filter-Pipeline vor und nach dem LLM-Aufruf
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 285)
import re

def sanitize_input(text: str) -> str:
    """Maskiere personenbezogene Daten VOR dem API-Call."""
    text = re.sub(r'\b[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}\b', '[NAME]', text)
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '[EMAIL]', text)
    text = re.sub(r'\+?\d{4,}', '[PHONE]', text)
    return text

def safety_check_output(text: str) -> dict:
    """Pruefe die Model-Ausgabe auf Safety-Probleme."""
    issues = []

    hate_keywords = {"hate_speech": [], "discrimination": []}
    for category, keywords in hate_keywords.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            issues.append({"type": category, "severity": "high"})

    if re.search(r'\d{3,}', text):
        issues.append({"type": "potential_pii", "severity": "medium"})

    return {
        "is_safe": len(issues) == 0,
        "issues": issues,
        "flagged_for_review": any(i["severity"] == "high" for i in issues),
    }

def safe_llm_query(user_input: str) -> str:
    """Komplette Safety-Pipeline."""
    sanitized = sanitize_input(user_input)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": sanitized}],
    )

    result = safety_check_output(response.choices[0].message.content)
    if result["flagged_for_review"]:
        return "Dieses Ergebnis wurde zur Sicherheitspruefung markiert " \
               "und bedarf manueller Freigabe."

    return response.choices[0].message.content

