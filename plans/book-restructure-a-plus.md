# Blueprint: Become an AI Engineer — A+ Editorial Restructure

**Objective**: Transform the manuscript into the best AI Engineering book in German by applying the mandatory 4-stage pipeline to every chapter, restructuring to target TOC order, eliminating all redundancy, fixing evidence quality, and achieving Chip Huyen / Kleppmann / Alex Xu editorial standard.

**Current State**: 16 chapters + appendix + glossary, ~44k words, B- book grade per review
**Target State**: 16 chapters in new order, A+ editorial quality, zero redundancy, timeless, evidence-backed, continuous product narrative

---

## Phase 0: Master Inventory & Dependency Map

### Current Chapter Order (main.tex) vs Target Order

| Current # | File | Current Title | Target # | Target Position | Action |
|-----------|------|---------------|----------|-----------------|--------|
| 1 | 01_ai_engineer_rolle | Die AI Engineer Rolle | 1 | ✓ Keep first | Light polish |
| 2 | 02_vorgefertigte_modelle | Vorgefertigte Modelle | 2 | ✓ Keep second | Light polish |
| 3 | 03_modell_landschaft | Modell-Landschaft | 3 | ✓ Keep third | Light polish |
| 4 | 04_openai_api | OpenAI API | — | **DELETE** (merge into 03 as provider table) | Remove chapter |
| 5 | 05_token_verwaltung | Token-Management | 4 | Move to position 4 | Full pipeline (wrong opening story) |
| 6 | 06_prompt_design | Prompt Design | 5 | ✓ Keep position 5 | Polish (A- → A+) |
| 7 | 07_rag_vector_datenbanken | RAG | 7 | Move to position 7 | Polish (A- → A+) |
| 8 | 08_ai_agenten | AI Agenten | 8 | Move to position 8 | Condense + pipeline |
| 9 | 09_evaluation_metriken | Evaluation | 6 | **MOVE TO POSITION 6** | Full pipeline (best chapter) |
| 10 | 14_multimodale_ki | Multimodale KI | 9 | Move to position 9 | Full pipeline (wrong opening) |
| 11 | 11_inferenz_optimierung | Inference Optimization | 11 | Move to position 11 | Full pipeline (English title, wrong opening) |
| 12 | 12_caching_routing_guardrails | Caching/Routing/Guardrails | 10 | Move to position 10 | Full pipeline (wrong opening) |
| 13 | 13_modellanpassung | Fine-Tuning | 12 | Move to position 12 | Full pipeline (wrong opening) |
| 14 | 10_deployment_architektur | Deployment | 13 | Move to position 13 | Rename + pipeline (title overlap) |
| 15 | 15_mlops_observability | MLOps | 14 | Move to position 14 | Full pipeline (wrong opening, thin) |
| 16 | 16_security_governance | Security | 15 | Move to position 15 | Full pipeline (wrong opening) |
| App | appendix_production_checklist | Checklist | 16 | ✓ Keep last | Keep as-is (A-) |
| App | 13_glossar | Glossar | 17 | ✓ Keep last | Fix LaTeX + consistency |

### Redundancy Elimination Map (One-Topic Rule)

| Topic | Current Appearances | **Single Deep Home** | Other Chapters: Forward Ref Only |
|-------|---------------------|----------------------|----------------------------------|
| Prompt Injection | 01, 06, 07, 12, 16 | **16 (Security)** | 01, 06, 07: intuition + "see Ch 16" |
| Semantic Cache | 01, 05, 06, 12 | **12 (Caching)** | 01, 05, 06: intuition + "see Ch 12" |
| Structured Outputs | 01, 04, 06 | **06 (Prompt)** | 01, 04: intuition + "see Ch 6" |
| Temperature | 01, 04, 06 | **06 (Prompt)** | 01, 04: intuition + "see Ch 6" |
| RAG vs Fine-Tuning | 02, 07, 13 | **13 (Fine-Tuning)** matrix; 07 (when RAG) | 02, 07: intuition + "see Ch 13" |
| Cost Optimization | 01, 05, 12 | **05 (Tokens)** + **12 (Caching)** | 01: intuition + "see Ch 5/12" |
| Observability | 01, 09, 10, 15 | **09 (Evaluation)** quality; **15 (MLOps)** ops | 01, 10: intuition + "see Ch 9/15" |
| Routing | 01, 05, 12 | **12 (Caching)** | 01, 05: intuition + "see Ch 12" |
| Token Pricing | 01, 05, 12 | **05 (Tokens)** | 01, 12: intuition + "see Ch 5" |
| German Token Factor | 01 (1.3x), 02 (1.8x), 05 (1.4-2x) | **05 (Tokens)** single number | Remove from 01, 02 |
| Halluzination | 01, 06, 07, 16 | **07 (RAG)** + **16 (Security)** | 01, 06: intuition + "see Ch 7/16" |

### Evidence Quality Violations (Must Fix Every Number)

| Number | Chapter | Required Context Missing |
|--------|---------|--------------------------|
| 94% Accuracy / Hit Rate | 04, 05, 06, 07, 13, 15, 16 | Baseline, n, dataset, metric definition, what changed, limitations |
| $400→$12 / $450→$38 | 04, 05, 07, 13, 15, 16 | Same story reused — each chapter needs OWN production incident |
| 67%→94% Hit Rate | 05, 07, 13, 15, 16 | Copied RAG story — delete from 05, 13, 15, 16 |
| 40-60% Cost Reduction | 01, 05, 12 | No traffic mix, no false positive rate, no scope |
| German token factor 1.3/1.8/1.4-2x | 01, 02, 05 | Inconsistent — unify to single range in Ch 05 only |

---

## Phase 1: P0 Integrity Fixes (Sprint 1 — Can run in parallel across chapters)

### 1.1 Fix Broken LaTeX Commands
- **Files**: 01, 06, 07, 13_glossar
- **Issues**: `\end{praxishinwisus}`, `\end{praxish` truncated, `\begin{praxishinweisEnv}` vs `\end{praxishinwisus}`
- **Action**: Search/replace all malformed environments

### 1.2 Fix Label Collision
- **Files**: 02_vorgefertigte_modelle.tex:209 (`tab:api-kosten`), 05_token_verwaltung.tex:209 (`tab:api-kosten`)
- **Action**: Rename one to `tab:api-kosten-modelle` and `tab:api-kosten-tokens`

### 1.3 Fix Wrong Chapter Teasers
- **Files**: 01 (teaser says "Prompt Engineering", TOC says "Pretrained Models"), 02 (same), 08 (teaser→Evaluation, TOC→Multimodal)
- **Action**: Align each chapter's closing `\autornotiz` teaser with actual next chapter in new TOC

### 1.4 Replace Copied Author Notes (Critical Trust Issue)
| Chapter | Current (Copied) | Required: Unique Production Story |
|---------|------------------|-----------------------------------|
| 05 | RAG E-Commerce (67%→94%, $450→$38) | **Token story**: $/query, max_tokens, history compression |
| 13 | RAG E-Commerce (same) | **FT story**: Format/Style, catastrophic forgetting, eval before/after |
| 15 | RAG E-Commerce (same) | **MLOps story**: Traces, SLOs, cost alerts, prompt drift |
| 16 | RAG E-Commerce (same) | **Security story**: Injection, PII leak, agent spend |

### 1.5 Unify German Token Factor
- **Decision**: Use "1.4–2x" in Chapter 05 only; remove from 01, 02
- **Action**: Edit 01 (line 81: 1.3x → remove), 02 (line 116: 1.8x → remove), 05 keeps 1.4–2x

---

## Phase 2: Structural Restructure (Sprint 2)

### 2.1 Delete Chapter 04 (OpenAI API)
- **Reason**: OpenAI-centric violates provider-agnostic promise; content merges into Ch 03 as comparison table
- **Action**: Remove `\input{chapters/04_openai_api}` from main.tex; migrate "Chat Completions Contract" provider-agnostic section to Ch 03; keep OpenAI as reference implementation only in tables

### 2.2 Reorder main.tex to Target Structure

```latex
% TEIL 1: GRUNDLAGEN VERSTEHEN
\part{Grundlagen verstehen}
\chapter{Die AI Engineer Rolle}           \input{chapters/01_ai_engineer_rolle}
\chapter{Vorgefertigte Modelle}            \input{chapters/02_vorgefertigte_modelle}
\chapter{Modell-Landschaft}                \input{chapters/03_modell_landschaft}

% TEIL 2: MIT DEM LLM SPRECHEN
\part{Mit dem LLM sprechen}
\chapter{Token-Management und Kosten}      \input{chapters/05_token_verwaltung}
\chapter{Prompt Design}                    \input{chapters/06_prompt_design}
\chapter{Evaluation und Metriken}          \input{chapters/09_evaluation_metriken}

% TEIL 3: DEM LLM KONTEXT UND HÄNDE GEBEN
\part{Dem LLM Kontext und Hände geben}
\chapter{RAG und Vector Datenbanken}       \input{chapters/07_rag_vector_datenbanken}
\chapter{AI Agenten}                       \input{chapters/08_ai_agenten}
\chapter{Multimodale KI}                   \input{chapters/14_multimodale_ki}

% TEIL 4: PRODUCTION LAYER
\part{Production Layer}
\chapter{Caching, Routing und Guardrails}  \input{chapters/12_caching_routing_guardrails}
\chapter{Inference Optimization}           \input{chapters/11_inferenz_optimierung}
\chapter{Model Customization}              \input{chapters/13_modellanpassung}

% TEIL 5: IN PRODUKTION BRINGEN
\part{In Produktion bringen}
\chapter{Deployment-Architekturen}         \input{chapters/10_deployment_architektur}
\chapter{MLOps und Observability}          \input{chapters/15_mlops_observability}
\chapter{Security, Governance, Responsible AI} \input{chapters/16_security_governance}

% ANHANG
\appendix
\chapter{Production Checklist}             \input{chapters/appendix_production_checklist}
\chapter{Glossar}                          \input{chapters/13_glossar}
```

### 2.3 Rename Chapters for Consistency
- 10_deployment_architektur → **Deployment-Architekturen und Betriebsmuster** (remove "Observability/Security" from title)
- 11_inferenz_optimierung → **Inference-Optimierung und Serving** (German title)
- 13_modellanpassung → **Model Customization — Fine-Tuning und Adaptation** (keep bilingual or full German)
- 14_multimodale_ki → **Multimodale KI — Vision, Audio und Video**

### 2.4 Fix Cross-References After Move
- Update all `\ref{chap:...}` and `\label{chap:...}` after reorder
- Verify no `??` in PDF after build

---

## Phase 3: Chapter-by-Chapter Pipeline Execution

**Execution Order** (dependencies considered):
1. **09_evaluation_metriken** → moves to position 6, highest priority (strongest chapter, sets evaluation mindset early)
2. **05_token_verwaltung** → moves to position 4, needs new opening story
3. **06_prompt_design** → position 5, polish only (A- → A+)
4. **07_rag_vector_datenbanken** → position 7, polish only (A- → A+)
5. **08_ai_agenten** → position 8, condense 1180 lines → ~600
6. **14_multimodale_ki** → position 9, new opening + couple to RAG
7. **12_caching_routing_guardrails** → position 10, security guards → Ch 16
8. **11_inferenz_optimierung** → position 11, clarify audience + skip box
9. **13_modellanpassung** → position 12, new FT story
10. **10_deployment_architektur** → position 13, rename + scope cut
11. **15_mlops_observability** → position 14, beef up or merge
12. **16_security_governance** → position 15, new incident story
13. **01_ai_engineer_rolle** → light polish, reduce 24 reality checks
14. **02_vorgefertigte_modelle** → remove duplicate pre-training explanation
15. **03_modell_landschaft** → provider prices to tables, MCP timing warning
16. **13_glossar** → fix LaTeX + consistency check

### Per-Chapter Pipeline (MANDATORY — No Stage Skipped)

For EACH chapter above, execute in sequence:

#### Stage 1: writing-researcher Agent
```
Input: Chapter file + neighbor chapters + main.tex order + this plan + review feedback
Output: research/<name>-a-plus-research.md
Required sections:
- Research Report (accuracy, outdated, missing concepts)
- Missing Topics
- Outdated Content (model versions, 202x refs)
- Duplicate Content (with specific line refs to other chapters)
- Suggested Improvements
- Trust Issues (unsupported numbers, copied stories)
- Required Evidence (every number needs: metric, baseline, n, dataset, scope, what changed, limitations)
- Cross-Chapter Dependencies (what this chapter must reference, what must reference it)
```

#### Stage 2: outline-writer Agent
```
Input: Research report + this plan's redundancy map + target skeleton
Output: research/<name>-a-plus-outline.md
Required skeleton (all 13 sections):
1. Why this matters
2. Mental Model
3. Architecture
4. Core Concepts
5. Production Example (NEW unique story per chapter)
6. Trade-offs
7. Failure Modes
8. Evaluation
9. Best Practices
10. Anti-Patterns
11. Production Checklist
12. Exercises
13. Further Reading
PLUS: Remove duplicated sections, improve transitions, merge overlaps, split overload, continuous product narrative
```

#### Stage 3: chapter-writer Agent
```
Input: Approved outline
Output: REWRITTEN chapters/<nr>_<name>.tex
Requirements:
- German body text; senior AI engineer voice
- Mechanisms over buzzwords
- Architecture before implementation
- Realistic production examples
- Trade-offs + failure modes mandatory
- Code labeled [Production Ready] or [Didactic Example]
- Provider-agnostic prose; provider specifics ONLY in tables
- Original production story for THIS chapter (no reused anecdotes/metrics/intros)
- Continuous product evolution (same app across book)
- Delete filler aggressively
- LaTeX compiles clean
```

#### Stage 4: writing-editor Agent
```
Input: Rewritten chapter
Output: research/<name>-a-plus-review.md
Actions:
- Remove redundancy, improve readability/transitions/pacing/consistency
- Simplify, strengthen arguments
- Verify terminology, refs, LaTeX, tables, listings, glossary
- Unique labels; every figure referenced; every metric explained
- Delete duplicated anecdotes/definitions/diagrams
- MAY freely delete content if it improves book
```

#### Quality Gate (Chapter Complete Only If ALL True)
- [ ] No duplicated explanations/anecdotes
- [ ] No unsupported numerical claims
- [ ] Consistent terminology
- [ ] LaTeX clean (no TODOs/placeholders; labels/refs OK)
- [ ] No unnecessary provider bias
- [ ] Important concepts have trade-offs
- [ ] Production recommendations have rationale
- [ ] Integrates into continuous book narrative
- [ ] A+ editorial quality

**On Failure**: Send back to appropriate stage (3 or 2) — do not declare complete.

---

## Phase 4: Continuous Narrative Design

### The Single Product Story (Evolves Across All Chapters)

**Product**: "SupportPilot" — AI-powered customer support platform for B2B SaaS

| Chapter | Product Evolution | Engineering Focus |
|---------|-------------------|-------------------|
| 01 (Role) | Simple chatbot answering FAQs | Role definition, architecture sketch |
| 02 (Models) | Provider abstraction layer | Model selection, multi-provider client |
| 03 (Landscape) | Cost tracking dashboard | Model routing, provider comparison |
| 04 (Tokens) | Token budgeting per conversation | Context management, compression |
| 05 (Prompts) | Structured classification + extraction | Prompt registry, golden set, eval pipeline |
| 06 (Eval) | CI/CD gate for prompt changes | Golden set, LLM-as-judge, regression detection |
| 07 (RAG) | Product knowledge base integration | Chunking, hybrid search, re-ranking, citations |
| 08 (Agents) | Action-taking agent (refunds, lookups) | Tool use, loop limits, HITL for critical actions |
| 09 (Multimodal) | Screenshot/document analysis | Vision RAG, frame sampling, OCR fallback |
| 10 (Caching) | Semantic cache for repeated queries | KV-cache, response cache, semantic cache, router |
| 11 (Inference) | Self-hosted Llama for PII data | vLLM, quantization, speculative decoding |
| 12 (Fine-Tuning) | SQL generator for analytics queries | LoRA/QLoRA, forgetting check, multi-LoRA serving |
| 13 (Deploy) | Kubernetes deployment with canary | FastAPI, circuit breaker, multi-region failover |
| 14 (MLOps) | Full observability + drift detection | Tracing, SLOs, cost alerts, prompt versioning |
| 15 (Security) | Injection defense, PII masking, audit | Input/output guards, RLS, incident runbooks |

**Rules**:
- Each chapter's production example advances SupportPilot
- No disconnected mini-projects
- Code in Ch N builds on Ch N-1 (import previous modules)
- Metrics/dashboard from Ch 6 used in Ch 14
- RAG from Ch 7 used in Ch 9 (Vision RAG)
- Agent from Ch 8 uses tools from Ch 10 (caching) and Ch 13 (deployment)

---

## Phase 5: Global Consistency Pass

After all chapters pass quality gate:

### 5.1 Terminology Audit
- Single German term per concept (e.g., "Kontextfenster" not "Context Window" mixed)
- Glossary definitions match chapter usage
- No English terms in German prose unless in comparison tables

### 5.2 Notation Consistency
- Token counts: always `1.000` (German) not `1,000`
- Costs: always `EUR` not `$` in body text (tables may show both)
- Latency: always `ms` with p50/p95/p99 specified
- Code: Python 3.11+ type hints, Pydantic v2, OpenAI SDK 1.x

### 5.3 LaTeX Build Verification
```bash
docker exec become-ai-book-dev latexmk -xelatex -outdir=_build main.tex
# Must complete with ZERO warnings
# No ?? in cross-refs
# All labels unique
```

### 5.4 Spell Check (VS Code German + en-US)
- Run in devcontainer
- Fix all flagged items

---

## Execution Plan: Step Breakdown

### Step 1: P0 Integrity Fixes (Parallel across chapters)
- [ ] 1.1 Fix broken LaTeX in 01, 06, 07, 13_glossar
- [ ] 1.2 Fix label collision tab:api-kosten (02, 05)
- [ ] 1.3 Fix chapter teasers (01, 02, 08)
- [ ] 1.4 Replace 4 copied author notes (05, 13, 15, 16)
- [ ] 1.5 Unify German token factor (remove from 01, 02)

**Verification**: `latexmk` clean build, grep for `praxishinwisus`, `tab:api-kosten` duplicates

### Step 2: Structural Restructure
- [ ] 2.1 Delete Ch 04 from main.tex, migrate contract section to Ch 03
- [ ] 2.2 Reorder main.tex to target structure
- [ ] 2.3 Rename chapter titles in main.tex
- [ ] 2.4 Fix all cross-references after move

**Verification**: TOC matches target order, no `??` refs, builds clean

### Step 3: Chapter Pipeline — Batch 1 (Evaluation, Tokens, Prompt, RAG)
For each: Research → Outline → Write → Edit → Quality Gate
- [ ] 09_evaluation_metriken (move to pos 6)
- [ ] 05_token_verwaltung (move to pos 4)
- [ ] 06_prompt_design (polish at pos 5)
- [ ] 07_rag_vector_datenbanken (polish at pos 7)

### Step 4: Chapter Pipeline — Batch 2 (Agents, Multimodal, Caching, Inference, FT)
- [ ] 08_ai_agenten (condense + pipeline at pos 8)
- [ ] 14_multimodale_ki (pipeline at pos 9)
- [ ] 12_caching_routing_guardrails (pipeline at pos 10)
- [ ] 11_inferenz_optimierung (pipeline at pos 11)
- [ ] 13_modellanpassung (pipeline at pos 12)

### Step 5: Chapter Pipeline — Batch 3 (Deploy, MLOps, Security, Foundation)
- [ ] 10_deployment_architektur (rename + pipeline at pos 13)
- [ ] 15_mlops_observability (pipeline at pos 14)
- [ ] 16_security_governance (pipeline at pos 15)
- [ ] 01_ai_engineer_rolle (light polish)
- [ ] 02_vorgefertigte_modelle (light polish)
- [ ] 03_modell_landschaft (light polish)

### Step 6: Appendix & Glossary
- [ ] 13_glossar (fix LaTeX + consistency)

### Step 7: Global Consistency & Final Build
- [ ] Terminology audit
- [ ] Notation consistency
- [ ] Full clean build in Docker
- [ ] VS Code spellcheck pass
- [ ] Final quality gate checklist

---

## Anti-Patterns to Avoid (Per Blueprint Catalog)

| Anti-Pattern | Prevention |
|--------------|------------|
| **Linear edit pass** | Never edit chapters sequentially start-to-finish. Each chapter through full pipeline independently. |
| **Skipping stages** | Every chapter MUST pass all 4 agents. No "good enough" shortcuts. |
| **Reusing anecdotes** | Track used stories in `research/used-stories.md` — check before writing |
| **Unverified numbers** | Every number requires measurement framework block — enforce in research stage |
| **Provider bleed** | Prose must be provider-agnostic; only tables get specific names |
| **Cross-ref drift** | After every main.tex reorder, full rebuild + `grep -r "??\|undefined"` |
| **Scope creep** | Chapters 01, 10, 13 must CUT scope (per review) — enforce via outline approval |

---

## Success Criteria

**Book-Level**:
- [ ] Target TOC order implemented
- [ ] Zero duplicated explanations (one-topic rule enforced)
- [ ] Every number has measurement context or labeled "illustrative"
- [ ] Zero 202x/version references in prose (tables only with date footnote)
- [ ] Provider-agnostic prose throughout
- [ ] Single continuous product narrative (SupportPilot)
- [ ] Clean LaTeX build, zero warnings
- [ ] A+ editorial quality comparable to Huyen/Kleppmann/Xu/O'Reilly

**Reader Outcome**: Finishes thinking *"I now understand how production AI systems are engineered, evaluated, deployed, monitored and improved"* — not *"I learned many AI tools."*

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Chapter pipeline takes 3-4 iterations | High | Timeline | Parallelize batches; strict quality gate prevents rework |
| Cross-ref breakage after reorder | High | Build failure | Automated verification after Step 2 |
| Research finds major gaps requiring new content | Medium | Scope | Outline stage catches; writer fills from expertise |
| Tone inconsistency across chapters | Medium | Quality | Editor stage enforces; shared voice guide in research |
| Docker build environment issues | Low | Block | Verify devcontainer works before Step 1 |

---

## Next Actions

1. **User confirms plan** → Proceed to Step 1 (P0 fixes)
2. **Create tracking files**: `research/used-stories.md`, `research/redundancy-map.md`
3. **Execute Step 1** (can be done in single session — 5 parallel fixes)
4. **Report Step 1 complete** → User approval → Step 2

---

*Plan generated per Blueprint skill. Each step is self-contained with verification commands for cold-start execution.*