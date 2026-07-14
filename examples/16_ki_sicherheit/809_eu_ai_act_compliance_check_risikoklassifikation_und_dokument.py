# EU-AI-Act-Compliance-Check: Risikoklassifikation und Dokumentationspflichten automatisieren
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 809)
from enum import Enum

class RiskClass(Enum):
    PROHIBITED = "prohibited"
    HIGH = "high-risk"
    GPAI = "gpai"
    TRANSPARENCY = "transparency"
    MINIMAL = "minimal"

class AIActCompliance:
    def __init__(self, system_name: str, risk_class: RiskClass):
        self.system_name = system_name
        self.risk_class = risk_class
        self.controls = []

    def check_requirements(self) -> dict:
        requirements = {
            "risk_management": self.risk_class in [
                RiskClass.HIGH, RiskClass.GPAI],
            "tech_documentation": self.risk_class in [
                RiskClass.HIGH, RiskClass.GPAI],
            "human_oversight": self.risk_class == RiskClass.HIGH,
            "conformity_assessment": self.risk_class == RiskClass.HIGH,
            "transparency": self.risk_class in [
                RiskClass.TRANSPARENCY, RiskClass.GPAI],
        }
        return requirements

    def generate_annex_iv_doc(self) -> dict:
        return {
            "system": self.system_name,
            "purpose": "Beschreibung des Verwendungszwecks",
            "data_sources": ["Trainingsdaten", "Validierungsdaten"],
            "performance_metrics": {"accuracy": 0.0, "latency_ms": 0},
            "human_oversight": "Massnahmen zur menschlichen Aufsicht",
            "risk_management": "Risikomanagement-Prozess nach Art. 9",
        }

# Beispiel: Hochrisiko-KI-System prufen
compliance = AIActCompliance(
    "Kunden-Support-Agent", RiskClass.HIGH
)
reqs = compliance.check_requirements()
for req, needed in reqs.items():
    status = "BENOTIGT" if needed else "OPTIONAL"
    print(f"  {req}: {status}")
doc = compliance.generate_annex_iv_doc()
print(f"Anhang-IV-Dokumentation erstellt fuer {doc['system']}")

