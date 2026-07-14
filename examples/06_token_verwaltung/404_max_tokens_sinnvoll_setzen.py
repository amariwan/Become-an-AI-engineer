# max_tokens sinnvoll setzen
# Quelle: chapters/06_token_verwaltung.tex (Zeile 404)
TASK_MAX_TOKENS = {
    "classification":     50,
    "extraction":        200,
    "summarization":     512,
    "analysis":         1024,
    "code_generation":  2048,
    "creative_writing": 4096,
}

def get_max_tokens(task_type: str) -> int:
    return TASK_MAX_TOKENS.get(task_type, 512)

# Dynamisches max_tokens
def configure_request(task_type: str, user_input: str) -> dict:
    input_tokens = count_tokens(user_input)
    max_out = get_max_tokens(task_type)
    return {
        "max_tokens": max_out,
        "estimated_cost": estimate_cost(
            "openai", "gpt-4o", input_tokens, max_out
        ),
    }

