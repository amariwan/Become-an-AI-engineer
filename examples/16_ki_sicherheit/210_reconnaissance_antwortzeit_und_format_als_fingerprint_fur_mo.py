# Reconnaissance: Antwortzeit und Format als Fingerprint für Modell-Identifikation
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 210)
import time

def fingerprint_model(client, prompts: list[str]) -> dict:
    results = []
    for prompt in prompts:
        start = time.perf_counter()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
        )
        latency = time.perf_counter() - start
        content = response.choices[0].message.content
        results.append({
            "prompt": prompt[:30],
            "latency": round(latency, 3),
            "response_len": len(content),
            "first_chars": content[:20],
        })
    return results

prompts = [
    "Hallo",
    "Was ist 2+2?",
    "Erkläre Quantenphysik in einem Satz.",
]
fingerprints = fingerprint_model(client, prompts)
for r in fingerprints:
    print(f"{r['prompt']:30s} | {r['latency']:.3f}s | {r['response_len']:4d} chars")

