# Prompt-Caching mit Cache-Control
# Quelle: chapters/04_kontext_preise.tex (Zeile 373)
# Prompt-Caching reduziert Input-Kosten um bis zu 90%
# fur statische Prompt-Teile (System-Prompt, Few-Shot)

response = client.chat.completions.create(
    model="claude-sonnet-4",
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {
                        "type": "ephemeral"
                    },
                }
            ],
        },
        {
            "role": "user",
            "content": user_query,
        },
    ],
)

# Check Cache-Treffer
print(f"Cache Input: {response.usage.cache_read_input_tokens}")
print(f"Cache Create: {response.usage.cache_creation_input_tokens}")

