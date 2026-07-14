# Dependency-Audit: Sicherheitslücken in ML-Abhängigkeiten erkennen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 487)
import subprocess
import json

def audit_python_deps() -> list[dict]:
    """Fuehrt ein Sicherheitsaudit aller installierten Pakete durch."""
    result = subprocess.run(
        ["pip-audit", "--format", "json", "--desc"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0 and result.returncode != 1:
        print(f"pip-audit fehlgeschlagen: {result.stderr}")
        return []

    audits = json.loads(result.stdout)
    vulnerabilities = audits.get("vulnerabilities", [])
    for vuln in vulnerabilities:
        print(f"[!]  {vuln['name']}=={vuln['version']}: "
              f"{vuln.get('advisory', 'Unbekannt')}")

    return vulnerabilities

# Weitere Schutzmassnahmen:
# 1. pip-audit im CI/CD-Job ausfuehren
# 2. requirements.txt mit Hash-Pinning
# 3. Regelmaessige Ueberpruefung der Model-Registry-Eintraege

