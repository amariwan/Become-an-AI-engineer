# Zero-Shot Prompting
# Quelle: chapters/07_prompt_design.tex (Zeile 190)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "system",
        "content": (
            "Du klassifizierst Support-Tickets nach Prioritaet. "
            "Antworte JSON: priority (1-5), category "
            "(billing/technical/complaint), urgency (low/medium/high)."
        )
    }, {
        "role": "user",
        "content": "Meine Bestellung ist seit 2 Wochen nicht angekommen!"
    }],
)

