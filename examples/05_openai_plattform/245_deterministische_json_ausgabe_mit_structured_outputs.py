# Deterministische JSON-Ausgabe mit Structured Outputs
# Quelle: chapters/05_openai_plattform.tex (Zeile 245)
from pydantic import BaseModel, Field

class MovieInfo(BaseModel):
    title: str = Field(description="Filmtitel")
    genre: list[str] = Field(description="Genre-Kategorien")
    rating: float = Field(description="Bewertung von 1.0 bis 10.0")
    year: int = Field(description="Erscheinungsjahr")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Beschreibe Inception"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "movie_info",
            "schema": MovieInfo.model_json_schema(),
            "strict": True,
        }
    },
)

result = MovieInfo.model_validate_json(response.choices[0].message.content)
# Garantiert valides MovieInfo-Objekt -- keine Parser-Fehler mehr!

