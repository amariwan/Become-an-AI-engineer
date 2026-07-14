# Tool Use mit Anthropic Claude
# Quelle: chapters/09_ai_agenten.tex (Zeile 501)
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Wetter in Berlin?"}],
    tools=[{
        "name": "get_weather",
        "description": "Wetterdaten abrufen",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "country": {"type": "string"},
            },
            "required": ["city"],
        },
    }],
)

for block in response.content:
    if block.type == "tool_use":
        result = get_weather(**block.input)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            messages=response.messages + [{
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                }],
            }],
        )

