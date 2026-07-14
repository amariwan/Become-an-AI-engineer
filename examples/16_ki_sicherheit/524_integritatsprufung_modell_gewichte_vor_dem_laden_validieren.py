# Integritätsprüfung: Modell-Gewichte vor dem Laden validieren
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 524)
import hashlib
import json

def verify_model_integrity(filepath: str, expected_hash: str) -> bool:
    computed = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            computed.update(chunk)
    actual = computed.hexdigest()
    if actual != expected_hash:
        print(f"SIGNATURFEHLER: Erwartet {expected_hash[:16]}..., "
              f"erhalten {actual[:16]}...")
        return False
    return True

# Beispiel: Pruefsumme aus einem vertrauenswuerdigen Manifest
manifest = json.loads("manifest.json")
if verify_model_integrity("model.bin", manifest["sha256"]):
    print("Modell-Integritaet bestaetigt. Lade Modell...")
else:
    raise RuntimeError("Modell-Integritaetspruefung fehlgeschlagen!")

