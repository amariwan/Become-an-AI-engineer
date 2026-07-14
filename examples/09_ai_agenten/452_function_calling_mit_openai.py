# Function Calling mit OpenAI
# Quelle: chapters/09_ai_agenten.tex (Zeile 452)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Wetter fuer eine Stadt abrufen",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Stadtname"},
                    "country_code": {
                        "type": "string",
                        "enum": ["DE", "AT", "CH"],
                    },
                },
                "required": ["city", "country_code"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user",
               "content": "Wetter morgen in Berlin?"}],
    tools=tools,
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
result = get_weather(args["city"], args["country_code"])

# Ergebnis an das Model zurueckgeben
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Wetter morgen in Berlin?"},
        response.choices[0].message,
        {"role": "tool", "tool_call_id": tool_call.id,
         "content": json.dumps(result)},
    ],
    tools=tools,
)
print(response.choices[0].message.content)

