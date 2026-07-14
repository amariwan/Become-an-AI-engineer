# Prompt-Effizienz messen
# Quelle: chapters/07_prompt_design.tex (Zeile 454)
def prompt_efficiency_score(prompt: str, output: str,
                            task_quality: float) -> float:
    """Score: Hoeher ist besser (viele Tokens fuer wenig Qualitaet = schlecht)."""
    prompt_tokens = len(tiktoken.get_encoding("o200k_base").encode(prompt))
    return task_quality / max(prompt_tokens, 1) * 1000

# Beispiel
score_a = prompt_efficiency_score(prompts["lang"], outputs["lang"], 0.95)
score_b = prompt_efficiency_score(prompts["kurz"], outputs["kurz"], 0.92)
# score_b > score_a: 3% weniger Qualitaet, aber 60% weniger Tokens

