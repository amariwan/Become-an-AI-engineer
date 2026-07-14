# Canary Queries: Manipulation im Index frühzeitig erkennen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 707)
CANARY_QUERIES = {
    "interne Richtlinie zur Datenverarbeitung": "GT_001",
    "Ansprechpartner fuer Sicherheitsvorfaelle": "GT_002",
}

def check_index_integrity(vector_store, expected_results: dict) -> bool:
    all_ok = True
    for query, expected_id in expected_results.items():
        docs = vector_store.similarity_search(query, k=1)
        if not docs or docs[0].metadata.get("id") != expected_id:
            print(f"CANARY-FEHLER: Abfrage '{query[:40]}...' "
                  f"erwartete {expected_id}, "
                  f"erhielt {docs[0].metadata.get('id', '?') if docs else '?'}")
            all_ok = False
    return all_ok

# Taeglicher Integritaetscheck
if not check_index_integrity(vector_store, CANARY_QUERIES):
    print("ALARM: Index-Manipulation erkannt! Sofortige Untersuchung erforderlich.")

