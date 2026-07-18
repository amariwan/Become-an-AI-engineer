# Voice Profile: "Become an AI Engineer" — Chip Huyen Inspired

**Ziel:** Senior AI Engineer Stimme — persönlich, mechanistisch, anti-hype, produktions-erprobt.

---

## Kernprinzipien

| Prinzip | Was das heißt | Beispiel |
|---------|---------------|----------|
| **Persönlich aber nicht egozentrisch** | "Ich" für Erfahrung, nicht für Meinung | "Als ich 2022 RAG in Produktion brachte..." nicht "Ich finde RAG wichtig" |
| **Mechanismen > Adjektive** | Erkläre *warum*, nicht *dass* | "Few-Shot funktioniert durch Pattern Matching + Format Following + Attention Bias" nicht "Few-Shot ist besser" |
| **Zahlen & Belege** | Eigene Messwerte, konkrete Benchmarks | "47% Token-Reduktion bei <2% Recall-Verlust" nicht "erheblich weniger Tokens" |
| **Ehrlich über Unsicherheit** | "Das ändert sich", "Hier bin ich mir nicht sicher" | "Dieser Abschnitt ist experimentell — feel free to skip" |
| **Anti-Hype, pro-Pragmatismus** | Frameworks kritisch, Eigenbau bevorzugt | "Agent-Frameworks bringen mehr Bugs als Features in Produktion" |
| **System-Denken** | Architektur, Failure Modes, Evaluation | Nicht nur Prompt-Techniken, sondern Pipeline + Monitoring + Cost Control |
| **Respektiere Leserzeit** | TL;DR, Skip-Marker, überspringbare Tiefe | `\skipdeep{...}` für Deep Dives |

---

## Satz-Rhythmus

- **Kurz. Präzise. Dann Erklärung.**
- Eine Hauptaussage pro Absatz.
- Parenthetische nur für Qualifikation: "(best effort, keine Garantie)", "(OpenAI dokumentiert das nur als...)".
- Keine Floskeln: "Es ist wichtig zu beachten", "Man sollte beachten", "Grundsätzlich gilt".

---

## Vokabular — Nutzen vs. Vermeiden

| Nutzen | Vermeiden |
|--------|-----------|
| "In Produktion..." | "In der Praxis..." (zu vage) |
| "Mein Messwert: X" | "Studien zeigen..." (ohne Quelle) |
| "Der Mechanismus: ..." | "Der Grund ist..." |
| "Skip this if..." | "Optional können Sie..." |
| "Reality Check:" | "Wichtig:" |
| "Was ich damals nicht wusste:" | "Ein häufiger Fehler ist:" |
| "Baue X selbst, statt Y zu nutzen" | "Es empfiehlt sich..." |

---

## Struktur pro Kapitel (ergänzt um Voice-Elemente)

```
\chapter{Titel}
\label{chap:...}

% LERNZIELE (bleibt)

% MOTIVATION + \AUTORnotiz{...}  ← NEU: persönlicher Einstieg

% GRUNDLAGEN

% \skipdeep{TL;DR für Theorie-Abschnitt}  ← NEU

% THEORIE — mit Mechanismus-Erklärungen, nicht Listen

% PRAXIS — Code + \realitycheck{...}  ← NEU: Produktions-Erfahrung

% BEST PRACTICES

% ANTI-PATTERNS (bleibt, Gold wert)

% PERFORMANCE — mit eigenen Zahlen

% SICHERHEIT

% ZUSAMMENFASSUNG

% \AUTORnotiz{Was ich beim Schreiben gelernt habe / Was sich 2026 ändern wird}  ← NEU

% MERKE-BOX (bleibt)

% PRAXISPROJEKT (bleibt)

% INTERVIEWFRAGEN → "Was ich im Hiring frage"  ← UMRAHMEN

% RESSOURCEN (bleibt)
```

---

## LaTeX Environments (in `voice-environments.sty`)

```latex
\usepackage{chapters/voice-environments}

% Im Text:
\AUTORnotiz{Als ich 2023 zum ersten Mal RAG in Produktion brachte...}
% oder länger:
\begin{AUTORnotiz}[Mein Fehler]
  Als ich 2023 zum ersten Mal RAG in Produktion brachte...
\end{AUTORnotiz}

\reality{Agent-Frameworks sehen in Demos toll aus. In Produktion...}
% oder:
\begin{realitycheck}[Warum ich LangGraph nicht nutze]
  ...
\end{realitycheck}

\skipdeep{In-Context Learning = Pattern Matching + Format Following + Attention Bias.}
% oder:
\begin{skipbox}[Kurzfassung: Warum Few-Shot funktioniert]
  ...
\end{skipbox}
```

---

## Checkliste für neues Kapitel (vor Commit prüfen)

- [ ] Mindestens **eine `\AUTORnotiz`** mit konkreter Erfahrung (Jahr, Situation, Zahl)
- [ ] Mindestens **ein `\realitycheck`** mit Anti-Hype Statement + Begründung
- [ ] Mindestens **eine `\skipbox`** für Deep-Dive-Theorie
- [ ] **Keine** Bullet-Liste für "Warum X funktioniert" — stattdessen Mechanismus-Paragraf
- [ ] **Mindestens eine eigene Messwert/Benchmark** (auch wenn grob: "In meinem Setup...")
- [ ] Interviewfragen als **"Was ich frage:"** gerahmt, nicht anonyme Liste
- [ ] Am Ende: **\AUTORnotiz mit Ausblick** — was sich ändern wird

---

## Beispiel: Prompt Design Kapitel (Ausschnitt)

> **Statt:** "Warum Few-Shot besser ist als Zero-Shot" als Bullet-Liste
>
> **Chip-Style:**
>
> Few-Shot schlägt Zero-Shot aus drei messbaren Gründen:
>
> 1. **Format Following** — das Model kopiert das Output-Muster statt es zu erraten. In meinen Tests: 94% valides JSON mit 3 Examples vs. 67% ohne.
> 2. **Decision Boundary Anchoring** — deine Edge-Cases in den Examples setzen die Klassifikationsgrenze präziser als jede Instruktion. Ein "borderline billing/complaint" Beispiel im Few-Shot verschiebt die Grenze um ~15% Recall.
> 3. **Attention Bias** — die Examples wirken wie Spotlight: "Hier lang schauen, Rest ignorieren."
>
> \reality{Drei gut gewählte Edge-Cases schlagen 20 zufällige Samples. Qualität > Quantität.}
>
> \skipdeep{TL;DR: Few-Shot = Pattern Matching + Format Following + Attention Bias. Details unten.}

---

## Nicht verhandelbar (Hard Bans)

- ❌ "Man sollte", "Es ist wichtig", "Grundsätzlich gilt"
- ❌ Fake-Neugier: "Haben Sie sich je gefragt...?"
- ❌ "Nicht X, sondern Y" Konstruktionen
- ❌ "No fluff", "Kurz gesagt", "Zusammenfassend"
- ❌ Bait-Fragen am Abschnittsende
- ❌ Em-dash-Overload (Chip hasst das auch: "I would pay $100 to stop ChatGPT from using em dashes")

---

## Referenzen zum Nachlesen

- huyenchip.com/2025/01/07/agents.html — Struktur: TOC + Notes + "skip ahead" + Mechanismen
- huyenchip.com/2024/07/25/genai-platform.html — Architektur-Layer, Reality Checks
- huyenchip.com/2024/03/14/ai-oss.html — 900 Repos, eigene Zahlen, China/US Vergleich
- "AI Engineering" (O'Reilly 2025) — Buch-Version des Blogs
- eugeneyan.com/writing/informal-mentors-chip-huyen/ — Interview über Schreibprozess