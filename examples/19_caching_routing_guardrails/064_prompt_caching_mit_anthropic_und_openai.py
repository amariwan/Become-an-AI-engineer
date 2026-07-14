# Prompt Caching mit Anthropic und OpenAI
# Quelle: chapters/19_caching_routing_guardrails.tex (Zeile 64)
# Anthropic: Prompt Caching via cache_control
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,  # 2.000 Tokens, statisch
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": user_query}],
)
print(f"Cache: {response.usage.cache_creation_input_tokens > 0}")

# OpenAI: Prompt Caching (automatisch ab 1.024 Tokens Prefix)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ],
)
print(f"Cache Hit: {response.usage.prompt_tokens_details.cached_tokens > 0}")

