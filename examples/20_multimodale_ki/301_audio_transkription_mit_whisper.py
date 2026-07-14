# Audio-Transkription mit Whisper
# Quelle: chapters/20_multimodale_ki.tex (Zeile 301)
def transcribe_audio(audio_path: str, language: str = "de") -> dict:
    """Transkribiert eine Audiodatei mit Whisher."""
    from openai import OpenAI

    client = OpenAI()

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    # Segment-Timestamps fuer Alignment
    segments = [
        {
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
        }
        for seg in transcript.segments
    ]

    return {
        "full_text": transcript.text,
        "segments": segments,
        "duration_s": transcript.segments[-1].end,
    }

