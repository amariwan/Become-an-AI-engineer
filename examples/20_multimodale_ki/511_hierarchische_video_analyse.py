# Hierarchische Video-Analyse
# Quelle: chapters/20_multimodale_ki.tex (Zeile 511)
class HierarchicalVideoAnalyzer(VideoAnalyzer):
    """Zusammenfassungs-Pipeline fuer lange Videos."""

    def analyze_long_video(self, video_path: str) -> dict:
        # Phase 1: Segmente analysieren (alle 10s ein Frame)
        self.interval = 10.0
        frames = self.extract_frames(video_path, max_frames=50)

        # Phase 2: Frames in Gruppen zu je 5 teilen
        segments = []
        for i in range(0, len(frames), 5):
            group = frames[i:i+5]
            segment_content = [
                {"type": "text",
                 "text": "Fasse zusammen, was in diesen "
                         "Videosegmenten passiert."},
            ]
            for f in group:
                segment_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{f['base64']}",
                        "detail": "low",
                    },
                })

            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user",
                          "content": segment_content}],
                max_tokens=512,
            )
            segments.append({
                "segment": i // 5,
                "timestamp": group[0]["timestamp"],
                "summary": resp.choices[0].message.content,
            })

        # Phase 3: Gesamt-Zusammenfassung
        all_summaries = "\n".join(
            f"[{s['timestamp']}] {s['summary']}"
            for s in segments
        )
        final = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user",
                 "content": f"Erstelle eine zusammenhaengende "
                            f"Zusammenfassung dieses Videos:\n\n"
                            f"{all_summaries}"}
            ],
        )
        return {
            "segments": segments,
            "summary": final.choices[0].message.content,
            "total_segments": len(segments),
        }

