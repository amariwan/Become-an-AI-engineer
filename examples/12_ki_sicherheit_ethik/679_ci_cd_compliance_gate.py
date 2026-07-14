# CI-CD-Compliance-Gate
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 679)
class ComplianceGate:
    """CI/CD-Check: Blockiert High-Risk-Deployments ohne Doku."""

    def __init__(self):
        self.registry: dict[str, AISystemDocumentation] = {}

    def register_system(self, doc: AISystemDocumentation):
        self.registry[doc.name] = doc

    def check_deployment(self, system_name: str) -> dict:
        doc = self.registry.get(system_name)
        if not doc:
            return {
                "allowed": False,
                "reason": "System nicht registriert",
            }

        risk = doc.classify_risk()
        if risk == RiskLevel.UNACCEPTABLE:
            return {
                "allowed": False,
                "reason": "Unacceptable Risk -- nicht zulassig",
            }

        if risk == RiskLevel.HIGH:
            report = doc.generate_report()
            if not doc.performance_metrics:
                return {
                    "allowed": False,
                    "reason": "High Risk: Leistungsmetriken fehlen",
                }
            if not doc.human_oversight:
                return {
                    "allowed": False,
                    "reason": "High Risk: Human Oversight fehlt",
                }

        return {
            "allowed": True,
            "risk_level": risk.value,
        }

# CI/CD-Gate im Deployment-Prozess
gate = ComplianceGate()
gate.register_system(doc)

result = gate.check_deployment("ResumeScorer")
if not result["allowed"]:
    print(f"Deployment blocked: {result['reason']}")
    exit(1)
else:
    print(f"Deployment allowed (risk: {result['risk_level']})")

