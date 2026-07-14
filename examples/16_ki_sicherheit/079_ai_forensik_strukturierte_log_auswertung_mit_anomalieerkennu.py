# AI-Forensik: strukturierte Log-Auswertung mit Anomalieerkennung
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 79)
from collections import Counter
from datetime import datetime, timedelta
import hashlib

calls = [
    {"model": "gpt-4o", "prompt_hash": "abc123", "duration_ms": 220,
     "timestamp": datetime.now() - timedelta(hours=2)},
    {"model": "gpt-4o", "prompt_hash": "abc123", "duration_ms": 215,
     "timestamp": datetime.now() - timedelta(hours=1)},
    {"model": "gpt-4o", "prompt_hash": "xyz789", "duration_ms": 980,
     "timestamp": datetime.now() - timedelta(minutes=10)},
]

baseline_avg = sum(c["duration_ms"] for c in calls) / len(calls)
baseline_std = (
    sum((c["duration_ms"] - baseline_avg) ** 2 for c in calls)
    / len(calls)
) ** 0.5

anomalies = [
    c for c in calls
    if c["duration_ms"] > baseline_avg + 2 * baseline_std
]
if anomalies:
    print("ANOMALIE: Ungewoehnlich lange Ausfuehrungszeiten")
    for a in anomalies:
        print(f"  {a['timestamp']}: {a['duration_ms']}ms "
              f"(+{(a['duration_ms'] - baseline_avg):.0f}ms Abweichung)")

prompt_counts = Counter(c["prompt_hash"] for c in calls)
print("Haeufigste Prompt-Hashes:", prompt_counts.most_common(3))

