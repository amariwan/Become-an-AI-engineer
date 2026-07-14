# Multimodaler Input-Guard
# Quelle: chapters/20_multimodale_ki.tex (Zeile 614)
class MultimodalGuard:
    """Sicherheitsfilter fuer multimodale Eingaben."""

    def __init__(self):
        self.text_filter = InputGuard()  # aus Kapitel 19

    def check_image(self, image_b64: str) -> bool:
        """Prueft Bild auf Injection-Versuche."""
        import pytesseract
        from PIL import Image
        import io

        image = Image.open(io.BytesIO(base64.b64decode(image_b64)))

        # OCR-extrahierter Text
        ocr_text = pytesseract.image_to_string(image)

        # Injection-Check im OCR-Text
        suspicious = self.text_filter.check(ocr_text)
        if suspicious:
            logger.warning({
                "event": "image_injection_detected",
                "ocr_text": ocr_text[:200],
                "reason": suspicious,
            })
            return False

        return True

    def check_audio(self, audio_path: str) -> bool:
        """Prueft Audio auf ungewoehnliche Frequenzen."""
        import librosa

        y, sr = librosa.load(audio_path, sr=None)
        # Pruefung auf Ultraschall (Frequenzen > 20 kHz)
        # Vereinfachte Implementierung
        return True

