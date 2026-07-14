# Video-Frame-Extraktion für LLM-Analyse
# Quelle: chapters/20_multimodale_ki.tex (Zeile 430)
import cv2
import base64
from openai import OpenAI
from pathlib import Path

class VideoAnalyzer:
    """Extrahiert Frames aus Video und analysiert sie multimodal."""

    def __init__(self, model: str = "gpt-4o",
                 frame_interval_s: float = 2.0):
        self.client = OpenAI()
        self.model = model
        self.interval = frame_interval_s

    def extract_frames(self, video_path: str,
                       max_frames: int = 30) -> list[dict]:
        """Extrahiert Frames in regelmaessigen Abstaenden."""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval)
        frames = []
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret or len(frames) >= max_frames:
                break

            if frame_count % frame_interval == 0:
                _, buffer = cv2.imencode(".jpg", frame, [
                    cv2.IMWRITE_JPEG_QUALITY, 85,
                ])
                b64 = base64.b64encode(buffer).decode()

                timestamp_s = frame_count / fps
                frames.append({
                    "timestamp_s": timestamp_s,
                    "timestamp": f"{int(timestamp_s//60)}m"
                                 f"{int(timestamp_s%60)}s",
                    "base64": b64,
                })

            frame_count += 1

        cap.release()
        return frames

    def analyze_video(self, video_path: str, prompt: str) -> str:
        """Video mit LLM analysieren (Frame-Sampling)."""
        frames = self.extract_frames(video_path)

        # Frames in API-Content umwandeln
        content = [{"type": "text", "text": prompt}]
        for frame in frames:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame['base64']}",
                    "detail": "low",  # low detail fuer viele Frames
                },
            })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            max_tokens=2048,
        )
        return response.choices[0].message.content

