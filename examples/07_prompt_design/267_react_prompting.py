# ReAct-Prompting
# Quelle: chapters/07_prompt_design.tex (Zeile 267)
REACT_SYSTEM = """Loese Aufgaben durch Nachdenken und Handeln.

Struktur:
  Thought: [Was muss ich tun?]
  Action: [Funktionsname]
  Action Input: [JSON-Parameter]
  Observation: [Ergebnis]
  ... (wiederholen bis fertig) ...
  Answer: [Endergebnis]

Tools:
  - search(query): Wissensdatenbank-Suche
  - calculate(expr): Berechnung
  - lookup_product(id): Produktdetails
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": REACT_SYSTEM},
        {"role": "user",
         "content": "Was kostet Produkt #12345? Gibt es Rabatte?"},
    ],
)

