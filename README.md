# Become an AI Engineer

**Der praxisorientierte Leitfaden für KI-Engineering 2026**

Von [Aland Baban](https://github.com/amariwan) · [tasiomind.dev](https://tasiomind.dev)

---

468 Seiten · 19 Kapitel · 190 Interviewfragen · CC BY-SA 4.0

Deutschsprachiges Lehrbuch — vom Software-Entwickler zum AI Engineer. Basierend auf der [AI Engineer Roadmap](https://roadmap.sh/ai-engineer) von roadmap.sh.

## Inhalt

| Teil | Titel | Kapitel |
|------|-------|---------|
| **I** | Grundlagen verstehen | 1–4: AI Engineer Rolle, vorgefertigte Modelle, Modell-Landschaft, Kontext & Pricing |
| **II** | Technik und Werkzeuge | 5–7: OpenAI Plattform, Token-Verwaltung, Prompt Design |
| **III** | LLMs in der Praxis | 8–10, 20: RAG & Vector DBs, AI Agents, Evaluation, Multimodale KI |
| **IV** | Production Layer | 17–19: Inference Optimization, Model Customization, Caching/Routing/Guardrails |
| **V** | In Produktion bringen | 11, 21, 12, 22, 16: Deployment, MLOps, KI-Sicherheit, Governance |

Jedes Kapitel enthält **10 Interviewfragen** mit ausführlichen Antworten auf Senior-Niveau (190 gesamt).

## Build

Läuft in Docker (VS Code Devcontainer oder manuell):

```bash
# Einmalig
docker build -t latex-book .devcontainer/

# Kompilieren (2× wegen cross-refs)
docker exec become-ai-book latexmk -xelatex -outdir=_build main.tex
docker exec become-ai-book latexmk -xelatex -outdir=_build main.tex

# Output: _build/main.pdf
```

Oder im laufenden Devcontainer:

```bash
docker exec <container-id> sh -c "cd /workspaces/Become-an-AI-engineer && latexmk -xelatex -outdir=_build main.tex"
```

## Projektstruktur

```
.
├── main.tex              # LaTeX-Quelldatei
├── chapters/             # 22 Kapitel als separate .tex-Dateien
├── imgs/                 # Buchabbildungen & Diagramme
├── scripts/              # Hilfsskripte (Konsistenz-Checks, Changelog)
├── skills/               # Claude Code / AI-Assistenten-Skills
├── .devcontainer/        # Docker-Build-Config (Ubuntu 24.04 + texlive-full)
├── .github/              # Issue/PR Templates
├── AGENTS.md             # Entwicklerdokumentation
├── interviewfragen.md    # Alle 190 Q&A im Markdown-Export
└── LICENSE               # CC BY-SA 4.0
```

## Lizenz

[CC BY-SA 4.0](LICENSE) — Frei teilbar und weiterverarbeitbar, auch kommerziell.
