# Grundlegende Chat Completions API-Nutzung
# Quelle: chapters/05_openai_plattform.tex (Zeile 150)
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ],
    temperature=0.7,
    max_tokens=1024,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

print(response.choices[0].message.content)
print(f"Tokens: input={response.usage.prompt_tokens}, "
      f"output={response.usage.completion_tokens}")

