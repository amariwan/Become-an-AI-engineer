# Prompt-Caching mit Anthropic
# Quelle: chapters/06_token_verwaltung.tex (Zeile 534)
# Anthropic: Explizites Cache-Control (ab Claude 3.5)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": user_input}],
)

# Cache-Statistiken auslesen
print(f"Cache Created: {response.usage.cache_creation_input_tokens}")
print(f"Cache Read: {response.usage.cache_read_input_tokens}")

