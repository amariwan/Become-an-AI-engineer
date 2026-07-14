# Compliance-Dokumentation-generieren
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 617)
def generate_compliance_documentation(
    system: AISystemDocumentation
) -> str:
    """Generiert die technische Dokumentation als Markdown."""

    report = system.generate_report()
    docs = f"""# Technische Dokumentation: {system.name} v{system.version}

## 1. Systembeschreibung
- Zweck: {system.purpose}
- Risikoklasse: {report['risk_level']}
- Klassifikationsdatum: {report['classification_date']}

## 2. Trainingsdaten
- Quellen: {report['training_data']['sources']}
- PII enthalten: {report['training_data']['has_pii']}
- Datenschutz-Folgenabschaetzung (DPIA): {'erforderlich'
    if report['training_data']['has_pii'] else 'nicht erforderlich'}

## 3. Leistungsmetriken
"""
    for metric, value in system.performance_metrics.items():
        docs += f"- {metric}: {value}\n"

    docs += f"""
## 4. Menschliche Aufsicht
- Implementiert: {report['human_oversight']}

## 5. Konformitaet
- CE-Kennzeichnung erforderlich: {report['conformity_assessment_required']}
"""
    return docs

