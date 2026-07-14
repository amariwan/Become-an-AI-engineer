# TTS mit mehreren Stimmen
# Quelle: chapters/20_multimodale_ki.tex (Zeile 389)
def generate_speech(text: str, voice: str = "alloy",
                    output_path: str = "output.mp3") -> str:
    """Erzeugt Sprachausgabe aus Text."""
    from openai import OpenAI

    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
        input=text,
        speed=1.0,
    )

    response.stream_to_file(output_path)
    return output_path

# Beispiel: Mehrsprachige Ansage
for lang, text, voice in [
    ("de", "Willkommen bei unserem Service.", "nova"),
    ("en", "Welcome to our service.", "alloy"),
    ("fr", "Bienvenue dans notre service.", "shimmer"),
]:
    generate_speech(text, voice=voice,
                    output_path=f"welcome_{lang}.mp3")

