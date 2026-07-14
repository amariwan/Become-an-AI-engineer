# H5-Modell-Scanning: Verdächtige benutzerdefinierte Schichten erkennen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 456)
import h5py

def scan_h5_model(filepath: str) -> list[str]:
    findings = []
    with h5py.File(filepath, "r") as f:
        def visit(name, obj):
            if isinstance(obj, h5py.Dataset):
                attr_keys = dict(obj.attrs).keys()
                for key in attr_keys:
                    val = obj.attrs[key]
                    decoded = val.decode() if isinstance(val, bytes) else str(val)
                    if any(s in decoded for s in ["lambda", "exec", "__import__"]):
                        findings.append(f"{name}: {key} -> {decoded[:100]}")

        f.visititems(visit)
    return findings

results = scan_h5_model("model.h5")
if results:
    print("[!]  GEFAEHRLICHE INHALTE GEFUNDEN:")
    for r in results:
        print(f"  {r}")
else:
    print("Keine verdaechtigen Custom-Layer gefunden.")

