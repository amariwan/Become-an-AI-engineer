# Become an AI Engineer

**Der praxisorientierte Leitfaden für KI-Engineering 2026**

Von [Aland Baban](https://github.com/amariwan) · [tasiomind.dev](https://tasiomind.dev)

---

Ein deutschsprachiges Lehrbuch, das dir den Weg vom Software-Entwickler zum AI Engineer zeigt. Basierend auf der offiziellen [AI Engineer Roadmap](https://roadmap.sh/ai-engineer) von roadmap.sh — praxisnah, konkret und direkt umsetzbar.

## Was erwartet dich?

Dieses Buch führt dich nicht in die Mathematik neuronaler Netze ein. Es setzt **Software-Engineering-Grundlagen** voraus (Python, TypeScript, REST APIs, Docker) und konzentriert sich auf das, was einen AI Engineer ausmacht: **den Umgang mit Large Language Models als Engineering-Aufgabe.**

### 📖 Struktur — 6 Teile · 22 Kapitel

| Teil | Titel | Kapitel |
|------|-------|---------|
| **I** | Grundlagen verstehen | 1–4: AI Engineer Rolle, vorgefertigte Modelle, Modell-Landschaft, Kontext & Pricing |
| **II** | Technik und Werkzeuge | 5–7: OpenAI-Plattform, Token-Management, Prompt-Design |
| **III** | LLMs in der Praxis | 8–12: RAG & Vector DBs, AI Agents, Evaluation, Deployment, KI-Sicherheit |
| **IV** | Production Layer | 13–19: Inferenz-Optimierung, Model-Anpassung, Caching/Routing/Guardrails |
| **V** | In Produktion bringen | 20–22: Multimodale KI, MLOps/Modelllebenszyklus, Verantwortliche KI-Governance |
| **VI** | Karriere | Glossar, Praxisprojekte, Bewerbungsprozess |

### 🎯 Für wen?

- Software-Entwickler:innen, die in KI einsteigen wollen
- AI Engineers mit Grundkenntnissen, die Production-Patterns vertiefen möchten
- Tech Leads, die das KI-Engineering-Ökosystem 2026 verstehen müssen

## Schnellstart — Buch kompilieren

Das Buch nutzt das [LiX thesis template](https://github.com/NicklasVraa/LiX). Der Build läuft **ausschließlich in Docker**:

```bash
# Container bauen (einmalig)
docker build -t latex-book .devcontainer/

# Buch kompilieren
docker exec become-ai-book latexmk -xelatex -outdir=_build main.tex

# Output: _build/main.pdf
```

[Details →](https://github.com/amariwan/Become-an-AI-engineer/blob/main/AGENTS.md)

## 🏗️ Projektstruktur

```
.
├── main.tex              # LaTeX-Quelldatei (LiX template)
├── chapters/             # 22 Kapitel als separate .tex-Dateien
├── imgs/                 # Buchabbildungen & Diagramme
├── .devcontainer/        # Docker-Build-Config für LaTeX
├── scripts/              # Hilfs-Skripte (PDF-Merge, EPUB-Export, etc.)
├── skills/               # Markdown-Skills für KI-Assistenten
├── .github/              # Issue/Pull Request Templates
└── AGENTS.md             # Projekt-Dokumentation
```

## 📄 Lizenz

[CC BY-SA 4.0](LICENSE) — Open Source: frei teilbar und weiterverarbeitbar, auch kommerziell.

---

*Viel Erfolg auf deinem Weg zum AI Engineer!* 🚀
