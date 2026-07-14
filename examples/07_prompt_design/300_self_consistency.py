# Self-Consistency
# Quelle: chapters/07_prompt_design.tex (Zeile 300)
from collections import Counter
import json

def self_consistent_answer(prompt: str, n: int = 5) -> str:
    answers = []
    for _ in range(n):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
        )
        answers.append(response.choices[0].message.content)

    # Majority Vote bei JSON-Objekten
    json_strs = [a for a in answers if a.startswith("{")]
    if json_strs:
        return Counter(json_strs).most_common(1)[0][0]
    return Counter(answers).most_common(1)[0][0]

