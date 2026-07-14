# Pickle forensisch mit pickletools analysieren
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 415)
import pickletools
import io

# Verdaechtige Pickle-Datei analysieren
with open("payload.pkl", "rb") as f:
    data = f.read()

print("=== Pickle-Bytecode Analyse ===")
pickletools.dis(data)

# Sicherheitscheck: Enthaelt das Pickle GLOBAL-REDUCE-Paare?
ops = list(pickletools.genops(io.BytesIO(data)))
for opcode, arg, pos in ops:
    if opcode.name == "GLOBAL":
        print(f"\n[!]  IMPORT erkannt: {arg}")
    if opcode.name == "REDUCE":
        print(f"[!]  REDUCE (Funktionsaufruf) erkannt bei Position {pos}")

# Empfohlen: Sicherheitsbibliothek Fickling verwenden
try:
    from fickling import Fickling
    fickling = Fickling(data)
    analysis = fickling.check()
    print(f"Fickling-Analyse: {'SICHER' if analysis.is_safe else 'GEFAEHRLICH'}")
except ImportError:
    print("Fickling nicht installiert. pip install fickling fuer bessere Analyse.")

