# AGENTS.md

German book "Become an AI Engineer — Der Schritt-für-Schritt-Leitfaden für 2026", based on roadmap.sh AI Engineer roadmap.

At session start, load matching skill(s) from `available_skills` — especially `latex-document-skill`, `find-docs`, `caveman`, `blueprint`.

## Entry points

The project uses the **LiX thesis Template** (`github.com/NicklasVraa/LiX`):

- `main.tex` — primary source. Uses `\documentclass{thesis}` and `\usepackage[all]{lix}`. Chapter files are included via `\input{chapters/*.tex}`. Code snippets use `listings` with `\lstdefinelanguage{Python}` and `\lstdefinelanguage{TypeScript}` predefined.
- `master_legacy.tex` — legacy book-class version. Kept for reference.

### LiX-specific commands

- `\toc` — table of contents
- `\h{Title}` — chapter heading (no number)
- `\l{FirstChar}{Rest}` — drop-cap first paragraph (lettrine)
- `\note{...}` — book note/blurb on title page
- `\blurb{...}` — book description
- `\cover{front.pdf}{back.pdf}` — book cover images
- `\lang{german}` — sets babel language
- `\authors{Name}` — author name
- `\license{CC}{by-sa}{4.0}` — Creative Commons license

## Build

**Must run inside Docker container.** Prebuilt container:

```bash
# Build (one-time)
docker build -t latex-book .devcontainer/

# Compile (container `become-ai-book-dev` muss laufen)
docker exec become-ai-book \
  latexmk -xelatex -outdir=_build main.tex

# Full clean (from host)
latexmk -xelatex -C

# Single chapter compile check: use `\includeonly{chapters/XX_filename}` in main.tex preamble
```

Output goes to `_build/`.

## Code style

- Language: German (babel `german` option). All text, section names, comments in German.
- Sectioning: `\h{}` for chapters, `\input{chapters/*.tex}` for content. Chapters organized in 5 parts via `\h{}` separators.
- Six parts (fixed order): Grundlagen verstehen, Technik und Werkzeuge, LLMs in der Praxis, Production Layer, In Produktion bringen, Karriere
- Add new chapter files under `chapters/` and reference them in `main.tex` under the correct part.
- Kapitel 15 (`chapters/15_bewerbungsprozess.tex`): Technisches "Production Proof"-Kapitel — System-Evaluation, Portfolio-Layer, Failure-Mode-Analyse. KEIN Karriere-Guide mehr (keine Gehaltstabellen, LinkedIn-Tipps, generische Bewerbungsstrategien).
- Neue Part 4 (Production Layer) eingefügt nach Part 3: Kapitel 17 (Inference Optimization), 18 (Model Customization), 19 (Caching/Routing/Guardrails).
- Code snippets: use `\begin{lstlisting}[language=Python|TypeScript]` (defined in main.tex preamble). No minted.
- No linter/formatter. LaTeX Workshop (VS Code extension) handles syntax checking.
- Snyk extension enabled in `.vscode/settings.json` — ignore for LaTeX.

## Quality checks (manual)

1. `latexmk -pdfxe -outdir=_build master.tex` — fix all warnings
2. Verify `\label{}` / `\ref{}` resolve (check for "??" in output)
3. VS Code German spellchecker (de-DE + en-US) configured via devcontainer

## Commit

- Prefix: `chapter:`, `style:`, `deps:`, `fix:`
- Verify compile before commit
