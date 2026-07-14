# LLM-as-a-Judge: Ein Modell bewertet die Antwort eines anderen
# Quelle: chapters/10_evaluation.tex (Zeile 283)
def llm_judge(query: str, answer: str, criteria: str) -> dict:
    """Ein starkes Model (GPT-4o) bewertet die Antwort eines anderen Models."""

    prompt = f"""Du bist ein Experte fuer Qualitaetsbewertung.
Bewerte die folgende Antwort auf einer Skala von 1-10.

Kriterien: {criteria}

Frage: {query}
Antwort: {answer}

Gib DEINUR eine Zahl zwischen 1 und 10 zurueck, keine Erklarungen."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    score = int(response.choices[0].message.content.strip())
    return {"score": max(1, min(10, score))}

# Anwendung: Bewertung der RAG-Qualitaet
for example in GOLDEN_DATASET:
    rag_answer = my_rag_chain.invoke(example["input"])
    judge_result = llm_judge(
        query=example["input"],
        answer=rag_answer,
        criteria="Faktenrichtigkeit, Vollstaendigkeit, Hoeflichkeit, Klarheit"
    )
    print(f"Score: {judge_result['score']}/10 fuer '{example['input'][:40]}...")

