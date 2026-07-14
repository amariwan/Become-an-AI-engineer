# Prompt-Caching mit OpenAI
# Quelle: chapters/06_token_verwaltung.tex (Zeile 515)
# OpenAI: Automatisches Caching fuer lange System-Prompts
# Caching passiert automatisch ab 1024 Token Input
# Gecachte Tokens kosten ~50% weniger

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},  # Gecached!
        {"role": "user", "content": user_input},
    ],
)

# Nutze response.usage fuer Cache-Statistiken
usage = response.usage
print(f"Cache Read: {usage.prompt_tokens_details.cached_tokens}")
print(f"Tokens Input (ohne Cache): {usage.prompt_tokens}")

