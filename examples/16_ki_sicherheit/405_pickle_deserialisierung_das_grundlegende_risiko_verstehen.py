# Pickle-Deserialisierung: Das grundlegende Risiko verstehen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 405)
import pickle

# UNSICHER: Pickle laedt nicht nur Daten, sondern fuehrt Bytecode aus
with open("modell.pkl", "rb") as f:
    model = pickle.load(f)  # Fuehrt beliebigen Code beim Laden aus

