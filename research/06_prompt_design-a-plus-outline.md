# Chapter 06 Outline — Prompt Design (A+ Target)

**Datei:** `chapters/06_prompt_design.tex`  
**Position:** Kapitel 5 (nach Token Management, vor Evaluation)  
**Produkt-Narrativ:** SupportPilot — B2B SaaS Support Automation (Klassifikation → Extraktion → Routing Pipeline)  
**Qualitätsziel:** A+ (Chip Huyen / Kleppmann / Alex Xu Standard)

---

## 1. Why this matters

**Kernthese:** Prompt Engineering ist nicht "Prompting" — es ist die **Haupt-Schnittstelle** zwischen Geschäftslogik und LLM-Verhalten. Jeder Token im Prompt kostet Geld, Latenz und 결정ungsqualität.

**SupportPilot Realität (Ersatz für kopierte Autorinnotiz):**
> 2023: SupportPilot v1 — Zero-Shot Klassifikation, gpt-3.5-turbo, temp 0.7, keine Validierung. 2.400 Tickets/Tag, $380/Tag API-Kosten, 63% Accuracy. Heute: Few-Shot (5 Edge-Cases), gpt-4o-mini-2024-07-18, temp 0.0, Pydantic + JSON Schema, Semantic Cache. 2.400 Tickets/Tag, $14/Tag, 94% Accuracy. Der Unterschied war nicht das Modell. Es war die Prompt-Pipeline.

**Messrahmen (gilt für JEDE Zahl in diesem Kapitel):**
- Metrik: Accuracy / Macro-F1 / Recall@P1 / Latency P99 / Cost per 1k tickets
- Baseline: Zero-Shot, gpt-3.5-turbo, temp 0.7
- n: 2.400 Tickets/Tag (Produktionsdaten, 30 Tage)
- Datensatz: SupportPilot E-Commerce-Kunde, DE/EN Tickets, stratifiziert nach Kategorie
- Scope: End-to-End Pipeline (Klassifikation → Extraktion → Routing)
- Was geändert: Prompt-Pipeline (Few-Shot, Structured Output, Caching, Versioning)
- Limitationen: Einzelkunde, spezifisches Schema, keine Verallgemeinerung auf andere Domänen

**Forward-Refs:** Ch1 (Grundlagen — JSON Mode Intro), Ch4 (Token Management — Budgets/Truncation), Ch7 (Evaluation — Golden Set Methodik)

---

## 2. Mental Model

**Drei-Layer-Prompt-Modell** (mechanistisch, nicht taxonomisch):
1. **Instruction Layer** — Was das Modell tun soll (Task Definition, Constraints, Output Format)
2. **Context Layer** — Was das Modell wissen muss (Few-Shot Examples, RAG Chunks, System State)
3. **Meta Layer** — Wie das Modell denken soll (Temperature, Reasoning Budget, Structured Output Schema)

**Prompt Engineering Pyramid** (Mechanismen, nicht Techniken):
- Basis: **In-Context Learning** — Pattern Matching + Format Following + Attention Bias (Min et al. 2022, Xie et al. 2022, Wei et al. 2023)
- Mitte: **Reasoning Elicitation** — Chain-of-Thought, ReAct, Self-Consistency
- Spitze: **System Integration** — Versioning, A/B Testing, Observability, Guardrails

**Key Insight:** Prompt = Code. Versioniert, getestet, deployed, gemonitort. Nicht "Prompting" als Chat-Aktivität.

**Backward-Ref:** Ch2/3 (LLM Fundamentals — Temperature, Logits, Sampling)

---

## 3. Architecture — Prompt Pipelines in Production

### 3.1 Pipeline Stages (Bestand)
```
Pre-Processing → Template Rendering → Token Budget Check → LLM Call → Post-Processing → Validation → Output
```
- Jinja2 Template Registry mit Hash-basiertem Caching
- Token-Budget-Check (Ch4 Patterns) vor Call
- Pydantic/Zod Validierung mit Retry-Loop (max 2, siehe §4.5)
- Strukturiertes Logging: Prompt Hash, Version, Latency, Tokens, Cost, Quality Metrics

### 3.2 Prompt Versioning Strategy (NEU — Critical Gap)
| Aspekt | Spezifikation |
|--------|---------------|
| **SemVer für Prompts** | MAJOR: Schema-Änderung (Output-Format), MINOR: Example hinzugefügt/entfernt, PATCH: Wording-Tweak |
| **Migration Guide Template** | Bei MAJOR: Input/Output Schema Diff, Breaking Changes, Rollback-Plan, Client-Migration Steps |
| **Backward Compatibility** | v3 Prompt muss v2 Output-Format verarbeiten können (falls Clients nicht migriert) |
| **Canary Deployment** | 5% Traffic → v3, Golden Set Re-Run, Business Metric Monitoring (Resolution Rate, CSAT), Auto-Rollback bei Regression >2% |
| **Prompt Registry API** | Runtime Version Selection: `GET /prompts/{name}/versions/{version}`, Feature Flags pro Kunde, A/B Bucket Assignment |

**Forward-Ref:** Ch19 (Production — Canary Deployments, Rollback Strategies)

### 3.3 A/B Testing Framework für Prompts (NEU)
```
Shadow Mode (Vor Rollout):
1. v1 (Production) + v2 (Shadow) parallel ausführen
2. Outputs vergleichen (Exact Match, Semantic Similarity, Business Metrics)
3. Statistische Gates: p < 0.01, Minimum Detectable Effect 3%, n ≥ 2000 pro Variante
4. Business Correlation: Accuracy Δ → Resolution Rate Δ → CSAT Δ (kausale Kette)

Online Evaluation (Nach Rollout):
- Continuous Golden Set Re-Run (täglich, 5% Sample)
- Drift Detection: Prompt Hash in Traces → Alert bei unerwarteter Version
- Automated Rollback: Macro-F1 < 0.88 ODER Recall@P1 < 0.92 ODER P99 Latency > 2s
```

### 3.4 Multilingual Prompt Strategy (NEU — SupportPilot B2B Context)
- **Language Detection → Prompt Routing** (nicht Translation)
- **Shared Few-Shot Examples** mit sprachspezifischen Varianten (DE/EN/FR/ES)
- **Token Factor Forward-Ref:** Ch4 (Deutsch ~1.3-1.5x Token Overhead vs English)
- **Registry:** `prompts/{task}/{language}/v{version}.j2`

---

## 4. Core Concepts — Mechanisms Deep Dive

### 4.1 In-Context Learning: Drei Mechanismen
1. **Pattern Matching** — Modell erkennt Task-Struktur aus Examples
2. **Format Following** — Ausgabe-Schema wird nachgeahmt (JSON, XML, Markdown)
3. **Attention Bias** — Examples lenken Attention auf relevante Input-Regionen

**Evidence:** Min et al. 2022 (Pattern Matching), Xie et al. 2022 (Format Following), Wei et al. 2023 (Attention Bias)

### 4.2 Temperature = Entropy Control
- **Prinzip:** Temperature skaliert Logits vor Softmax → kontrolliert Entropy der Token-Verteilung
- **0.0:** Gierig (argmax), aber NICHT bit-identisch (Server-side Batching, Race Conditions)
- **0.3-0.7:** Kreativität/Exploration (Brainstorming, Code Generation)
- **>1.0:** High Entropy (Diversität, aber Halluzinations-Risiko)

**Tabelle → Appendix A.3** mit Model/Date Stamp: `gpt-4o-mini-2024-07-18`, `gpt-4o-2024-08-06`, `claude-3-5-sonnet-20241022` — Preise/Verhalten datiert.

### 4.3 Few-Shot: Mechanismen + Edge-Case Mining Workflow (EXPAND)

**Drei Mechanismen (Bestand):**
1. Task Demonstration (Input→Output Mapping)
2. Format Anchoring (Schema Compliance)
3. Boundary Calibration (Edge Cases definieren Entscheidungsgrenzen)

**Edge-Case Mining Workflow (NEU — Konkreter Prozess):**
```
Wöchentlich (Automatisiert + Human-in-the-Loop):
1. Log: Jede Prediction + Ground Truth (Human Label ODER Delayed Feedback via Resolution)
2. Filter: Errors only → Embedding (text-embedding-3-small) + k-means (k=10-20)
3. Cluster Analysis: Für jeden Cluster → 1-2 repräsentative Hard Cases picken
4. Promotion: Zu Few-Shot Set hinzufügen → Golden Set Re-Run → Macro-F1 Δ > 0.5pp → Promote
5. Half-Life Tracking: Example Retirement nach 30 Tagen ohne Marginal Contribution (SHAP Value < 0.01)
```

**Evidence Template für Every Number:**
- 67% → 94% valid JSON: gpt-4o-mini-2024-07-18, n=500, Schema=TicketClassification, 3 Few-Shot vs 0, 95% CI [89%, 97%]
- +11pp Billing Recall (Overlap Example): Confusion Matrix Before/After, McNemar Test p<0.01, n=1200 Tickets

### 4.4 Receptivity Maximum (~2-4k Instruction Tokens)
- **Zitat:** Liu et al. 2024 "Lost in the Middle" + Instruction Saturation Papers (z.B. Zhou et al. 2024)
- **Mechanismus:** Attention Dilution — mittlere Instruktionen werden "vergessen"
- **Praxis:** Instruktionen < 2k Tokens halten, kritische Constraints an Anfang UND Ende wiederholen (Primacy/Recency)

### 4.5 Structured Output / JSON Mode — DEEP HOME (Ch6 owns this, Ch1/Ch4 forward-ref only)

**OpenAI Structured Outputs (GA 2024-08):**
```python
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "ticket_classification",
        "schema": TicketClassification.model_json_schema(),
        "strict": True  # Guaranteed valid JSON, constrained decoding
    }
}
```

**Anthropic Tool Choice Pattern:**
```python
tools = [{
    "name": "output_ticket_classification",
    "description": "Classify support ticket",
    "input_schema": TicketClassification.model_json_schema()
}]
tool_choice = {"type": "tool", "name": "output_ticket_classification"}
```

**Pydantic → JSON Schema Generation:**
- `model.model_json_schema()` → OpenAI strict mode kompatibel
- `Field(description="...")` → wird zu Schema Description (verbessert Compliance)

**Validation Retry Loop (Production Pattern):**
```python
max_retries = 2
for attempt in range(max_retries):
    try:
        result = await llm_call(prompt, response_format=schema)
        return TicketClassification.model_validate_json(result)
    except ValidationError as e:
        if attempt == max_retries - 1: raise
        prompt = add_retry_context(prompt, e.errors())
        # Cost: ~1.3x tokens per retry, aber 99.9%+ Valid JSON Rate
```

**Cost/Benefit:** Retry Loop kostet ~30% mehr Tokens, spart aber Downstream Parsing Errors (40% weniger, gpt-4o-mini, n=10k, CI [35%, 45%]).

**Strict vs Non-Strict Mode:** Strict = Constrained Decoding (langsamer, garantiert valide), Non-Strict = Post-Hoc Validation (schneller, ~94% valide ohne Few-Shot).

### 4.6 Automatic Prompt Optimization (APO) — State of the Art (Vertiefung / Skip-Box)
| Methode | Ansatz | Production Readiness |
|---------|--------|---------------------|
| **DSPy** (Khattab et al.) | Programmatische Prompt-Optimierung via Modules | Hoch — Databricks, production |
| **OPRO** (Yang et al. 2024) | LLMs optimieren Prompts für LLMs | Mittel — Research Stage |
| **PromptAgent / TextGrad** | Gradient-basierte Prompt-Optimierung | Niedrig — Experimental |
| **APE** (Zhou et al. 2023) | Automatic Prompt Engineer | Niedrig — Superseded |

**Placement:** Ende Theory Section als `\skipbox{Vertiefung: Automatische Prompt-Optimierung — Stand der Technik}`

---

## 5. Production Example — SupportPilot Pipeline Evolution (NEU — Unique Story)

**Nicht Claypot (bleibt als別 Lektion), nicht generische Zahlen — SupportPilot spezifisch:**

### 5.1 v1 (2023) — Zero-Shot Chaos
```
Prompt: "Classify this support ticket into: billing, technical, account, shipping, complaint"
Model: gpt-3.5-turbo, temp 0.7
Output: Freitext → Regex Parsing → 40% Parse Errors
Metrics: 63% Accuracy, $380/Tag, P99 3.2s
Pain: Keine Validierung, keine Versionierung, keine Observability
```

### 5.2 v2 (2024-Q1) — Few-Shot + Structured Output
```
Prompt: 5 Few-Shot Examples (inkl. 1 Overlap: billing+complaint)
Model: gpt-4o-mini-2024-07-18, temp 0.0
Output: JSON Schema (Pydantic strict mode) + Retry Loop (max 2)
Pipeline: Classification → Entity Extraction → Routing Decision
Metrics: 91% Macro-F1, Recall@P1 94%, $42/Tag, P99 1.8s
```

### 5.3 v3 (2024-Q3) — Production Hardening
```
Additions:
- Prompt Versioning (SemVer, Canary 5%)
- A/B Testing Framework (Shadow Mode, Statistical Gates)
- Edge-Case Mining (Wöchentlich, Clustering, Half-Life)
- Prompt Caching (OpenAI Auto ≥1024 Tokens, 50% Discount verified Nov 2024)
- Semantic Cache (Embedding Similarity >0.92, Hit Rate 34%)
- Prompt Efficiency Score CI Gate (Tokens per Quality Point)
- Injection Defense (XML Isolation + Pydantic + Moderation API)
Metrics: 94% Macro-F1, Recall@P1 96%, $14/Tag, P99 1.2s, 99.9% Uptime
```

### 5.4 Architecture Diagram (Textbeschreibung für LaTeX)
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Classify    │──▶│ Extract     │──▶│ Route       │
│ (v3.2.1)    │   │ (v2.1.0)    │   │ (v1.0.0)    │
│ 5-shot      │   │ 3-shot      │   │ Rule-based  │
│ JSON strict │   │ JSON strict │   │ (no LLM)    │
└─────────────┘   └─────────────┘   └─────────────┘
      │                │                │
      ▼                ▼                ▼
┌─────────────────────────────────────────────┐
│ Prompt Registry API (Version Selection)     │
│ - Canary 5% (Classification v3.3.0-rc1)     │
│ - Feature Flag: enterprise_customer=true    │
│ - Golden Set Daily Re-Run                   │
└─────────────────────────────────────────────┘
```

**Messrahmen für jede Pipeline-Stage:** Separate Golden Sets, separate Versioning, separate A/B Tests.

---

## 6. Trade-offs

| Decision | Option A | Option B | Decision Rule |
|----------|----------|----------|---------------|
| **Temperature** | 0.0 (Deterministisch) | 0.3-0.7 (Kreativ) | Classification/Extraction: 0.0. Generation/Summarization: 0.3-0.5 |
| **Few-Shot Count** | 3-5 Examples | 10-20 Examples | 5 ist Sweet Spot (Diminishing Returns >5, Liu et al. 2024). Mehr nur für Edge-Case Coverage. |
| **CoT vs Direct** | CoT (Reasoning) | Direct (Speed) | CoT nur bei Multi-Hop Reasoning (ReAct). Cost: 1.5-2x Latency, +10-20% Accuracy (Wang et al. 2023). |
| **Self-Consistency** | 5 Samples + Majority Vote | Single Sample | **Cost/Benefit Matrix (NEU):**<br>• P1 Ticket Routing: Ja (Kosten/Nutzen gerechtfertigt, +15% Recall@P1)<br>• Bulk Classification: Nein (5x Cost, +2% Macro-F1 nicht gerechtfertigt)<br>• Medical Coding: Ja (Regulatory)<br>• Fraud Detection: Ja (High Stakes) |
| **Structured Output Mode** | Strict (Constrained Decoding) | Non-Strict + Retry | Strict default. Non-Strict nur bei Latency-SLO < 500ms und Schema einfach. |
| **Prompt Compression** | LLMLingua-2 (2-5x Reduction) | Full Prompt | Compression nur bei >8k Input Tokens ODER Cost Critical (>$0.01/Call). Quality Loss <2% (LLMLingua-2 Paper). |
| **Versioning Granularity** | Per-Prompt File | Monorepo Prompt Registry | Registry ab 3+ Prompts, 2+ Engineers, Canary Bedarf. |

---

## 7. Failure Modes

| Failure Mode | Symptom | Detection | Mitigation |
|--------------|---------|-----------|------------|
| **Prompt Drift** | Accuracy degradiert langsam, Prompt Hash ändert sich unerwartet | Daily Golden Set Re-Run + Hash Alert in Traces | Auto-Rollback auf letzte stabile Version, Alert an Team |
| **Schema Violation** | Pydantic ValidationError > 1% Rate | Validation Metrics Dashboard | Retry Loop (max 2), Fallback auf Non-Strict Mode, Alert |
| **Few-Shot Poisoning** | Neues Example senkt Overall Accuracy | Golden Set Re-Run nach jedem Example-Add | A/B Test jedes neue Example, nur bei Δ > +0.5pp promoten |
| **Injection Success** | Malicious Output, Data Exfiltration | Moderation API + Output Schema Validation | XML Isolation, Pydantic Strict, Moderation API, Rate Limiting |
| **Context Overflow** | Truncation verliert kritische Instruktionen | Token Budget Check Pre-Call | Receptivity Limit (2-4k) einhalten, Priorisierung |
| **Semantic Cache Poisoning** | Falsche Cache Hits → Falsche Antworten | Cache Hit Audit (Sample 1% → Human Review) | Similarity Threshold 0.92+, TTL 24h, Cache Key includes Prompt Version |
| **Multilingual Drift** | DE Performance divergt von EN | Per-Language Golden Sets | Sprache-spezifische Few-Shot Sets, Separate Versioning |
| **Cost Explosion** | Self-Consistency / CoT unerwartet aktiv | Cost per 1k Calls Dashboard + Alert | Hard Limits pro Pipeline-Stage, Circuit Breaker |

---

## 8. Evaluation

### 8.1 Golden Set Methodology (Deep Home — Ch7 forward-ref)
- **Größe:** 200+ Cases (nicht 50-100) — stratifiziert nach Kategorie, Schweregrad, Sprache
- **Statistical Power:** 80% Power, α=0.05, MDE=3% → n ≥ 200 pro Variante
- **Metrics:** Macro-F1 (Primary), Recall@P1/P2 (Business Critical), Per-Class F1, Latency P50/P99, Cost per 1k
- **CI Gate:** Macro-F1 > 0.90, Recall@P1 > 0.95, P99 < 1.5s, Cost < $20/1k

### 8.2 LLM-as-a-Judge (Forward-Ref Ch7)
- Nur für subjektive Qualitäten (Tone, Completeness, Helpfulness)
- Calibration: Human Judge Agreement κ > 0.8 vor Deployment

### 8.3 Prompt Efficiency Score (CI Gate — NEU Enforcement)
```
Efficiency = Task_Quality / (Input_Tokens + Output_Tokens)
Task_Quality = Macro-F1 (0-1 scale)
CI Gate: Efficiency > 1.5 (Baseline v1: 1.2, v3: 3.8)
```
- Berechnet pro Prompt Version bei jedem Golden Set Run
- Regression → Build Failure

### 8.4 A/B Test Statistical Rigor (NEU)
- **Shadow Mode Duration:** 7 Tage minimum
- **Sample Size:** Power Analysis → n ≥ 2000 pro Variante
- **Significance:** p < 0.01 (Bonferroni korrigiert für multiple Metrics)
- **Business Metric Correlation:** Accuracy Δ → Resolution Rate Δ (Spearman ρ > 0.7)

### 8.5 Injection Test Suite (Praxisprojekt Update)
- 1000+ Tests: HackAPrompt Subset (500) + Custom Domain-Specific (500)
- Metrics: Detection Rate > 99%, False Positive Rate < 0.1%
- CI Gate: Zero Critical Injections in Test Suite

---

## 9. Best Practices

1. **Prompt = Code** — Versioniert (SemVer), Getestet (Golden Set), Deployed (Canary), Gemonitort (Drift Detection)
2. **Temperature 0.0 Default** — Für alle deterministischen Tasks (Classification, Extraction, Routing)
3. **Structured Output Strict Mode** — Pydantic/Zod Schema, Retry Loop max 2, Cost Accepted
4. **Few-Shot = 5 Examples** — 3 Typical + 1 Boundary + 1 Overlap (Edge-Case Mining workflow)
5. **Instruction Tokens < 2k** — Receptivity Maximum respektieren, Primacy/Recency nutzen
6. **Prompt Caching First** — OpenAI Auto (≥1024 Tokens), Anthropic Explicit — Zero Code Change, 50% Discount
7. **Semantic Cache Second** — Embedding Similarity >0.92, Hit Rate Tracken, TTL 24h
8. **Edge-Case Mining Weekly** — Clustering → Promotion → Half-Life Tracking
9. **Multilingual: Route, Don't Translate** — Sprache-spezifische Prompts, Shared Examples wo möglich
10. **Observability: Prompt Hash in JEDEM Trace** — Version, Tokens, Cost, Latency, Quality Metrics
11. **Injection Defense: Defense-in-Depth** — XML Isolation + Schema Validation + Moderation API
12. **Cost Tracking per Prompt Version** — Prompt Efficiency Score CI Gate

---

## 10. Anti-Patterns

| Anti-Pattern | Warum Schädlich | Besser |
|--------------|----------------|--------|
| **"Prompt Engineering" als Chat-Aktivität** | Nicht reproduzierbar, nicht versionierbar, nicht testbar | Prompt Pipeline als Code (Jinja2 Registry, Git, CI) |
| **Temperature > 0 für Classification** | Nicht-deterministisch, Flaky Tests, Debugging Hölle | Temperature 0.0, Structured Output Strict |
| **Few-Shot ohne Edge Cases** | Boundary Decisions falsch, Recall@P1 leidet | Edge-Case Mining Workflow (wöchentlich) |
| **Monolithische Prompts** | >4k Instruktion Tokens → Quality Collapse | Modulare Pipeline Stages (Classify→Extract→Route) |
| **Keine Versionierung** | Rollback unmöglich, A/B Testing unmöglich | SemVer + Git Tags + Registry API + Canary |
| **Golden Set = 50 Cases** | Unterpowered, flaky Metrics | 200+ stratifiziert, Power Analysis dokumentiert |
| **Self-Consistency überall** | 5x Cost für marginale Gains | Cost/Benefit Matrix: nur P1/High-Stakes |
| **Prompt Compression blind** | Quality Loss bei komplexen Reasoning Tasks | Nur bei >8k Tokens ODER Cost Critical, Quality Gate |
| **Injection Test = 10 Cases** | HackAPrompt zeigt 1000+ Attack Vectors | 1000+ Test Suite (HackAPrompt + Custom) |
| **Multilingual via Translation** | Token Overhead, Cultural Nuance Loss, Quality Drift | Language Detection → Prompt Routing |

---

## 11. Production Checklist (NEU — Mandatory vor Deploy)

### Pre-Deploy (CI Gates)
- [ ] **Golden Set Pass:** Macro-F1 > 0.90, Recall@P1 > 0.95, Per-Class F1 > 0.85
- [ ] **Latency SLO:** P99 < 1.5s (Classification), < 2.0s (Extraction)
- [ ] **Cost Budget:** < $20/1k Tickets (Blended)
- [ ] **Prompt Efficiency Score:** > 1.5 (Tokens per Quality Point)
- [ ] **Injection Test Suite:** 1000+ Tests, Detection > 99%, FP < 0.1%
- [ ] **Schema Validation:** 100% Valid JSON auf Golden Set (Strict Mode)
- [ ] **Multilingual Parity:** DE/EN/FR/ES Macro-F1 Δ < 3pp
- [ ] **Prompt Hash Logged:** In allen Traces, Version auflösbar

### Deploy (Canary)
- [ ] **Canary 5%:** Neue Version auf 5% Traffic, 24h Observation
- [ ] **Golden Set Re-Run:** Täglich während Canary, Auto-Rollback bei Regression
- [ ] **Business Metrics:** Resolution Rate, CSAT, Escalation Rate — No Regression
- [ ] **Cost Monitoring:** Cost per 1k Tickets Δ < 10% vs Baseline

### Post-Deploy (Ongoing)
- [ ] **Daily Golden Set Re-Run:** 5% Sample, Alert bei Macro-F1 < 0.88
- [ ] **Weekly Edge-Case Mining:** Clustering → Promotion → Half-Life Check
- [ ] **Monthly Prompt Audit:** Version Usage, Cost per Version, Retire Unused
- [ ] **Quarterly APO Evaluation:** DSPy/OPRO Benchmark vs Manual Prompts

---

## 12. Exercises (Praxisprojekt — SupportPilot Aligned)

### Exercise 1: Prompt Pipeline from Scratch (2-3h)
**Aufgabe:** Baue Classification → Extraction → Routing Pipeline für SupportPilot Ticket Sample (500 Tickets, DE/EN).
**Requirements:**
- Jinja2 Template Registry mit 3 Stages
- Pydantic Schemas + Strict JSON Mode + Retry Loop (max 2)
- Temperature 0.0, Few-Shot (3 Typical + 1 Boundary + 1 Overlap)
- Token Budget Check (Ch4) vor jedem Call
- Prompt Hash + Version in structured logs

**Acceptance:** Macro-F1 > 0.88, Recall@P1 > 0.92, P99 < 2s, 100% Valid JSON

### Exercise 2: A/B Test Framework (1-2h)
**Aufgabe:** Implementiere Shadow Mode Comparison v1 vs v2.
**Requirements:**
- Parallel Execution v1 (Prod) + v2 (Shadow)
- Statistical Gates: p<0.01, MDE 3%, n≥2000
- Business Metric Correlation (Accuracy → Resolution Rate)
- Automated Rollback Trigger

### Exercise 3: Edge-Case Mining Automation (2h)
**Aufgabe:** Wöchentlicher Pipeline für Failure Clustering → Example Promotion.
**Requirements:**
- Log Prediction + Ground Truth (simulated delayed feedback)
- Embedding + k-means Clustering (k=15)
- Representative Case Selection pro Cluster
- Golden Set Re-Run + Promotion Gate (Δ Macro-F1 > 0.5pp)
- Half-Life Tracking (SHAP Value < 0.01 → Retire)

### Exercise 4: Injection Defense Hardening (1h)
**Aufgabe:** Defense-in-Depth Implementation + Test Suite.
**Requirements:**
- XML Isolation Wrapper
- Pydantic Strict Mode Validation
- Moderation API Integration
- 1000 Test Cases (HackAPrompt 500 + Custom 500)
- Detection Rate > 99%, FP < 0.1%

### Exercise 5: Prompt Compression Benchmark (1h)
**Aufgabe:** LLMLingua-2 vs Full Prompt auf SupportPilot Pipeline.
**Requirements:**
- Compression Ratio, Quality Delta (Macro-F1), Latency Delta
- Decision: Compress Y/N basierend auf Cost/Benefit
- Document: When Worth It (>8k Tokens ODER Cost Critical)

---

## 13. Further Reading

### Papers (Core Mechanisms)
- Min et al. (2022) — "Rethinking the Role of Demonstrations in In-Context Learning"
- Xie et al. (2022) — "An Explanation of In-Context Learning as Implicit Bayesian Inference"
- Wei et al. (2023) — "Larger Language Models Do In-Context Learning Differently"
- Liu et al. (2024) — "Lost in the Middle: How Language Models Use Long Contexts"
- Wang et al. (2023) — "Self-Consistency Improves Chain of Thought Reasoning"
- Yang et al. (2024) — "Large Language Models as Optimizers (OPRO)"
- Khattab et al. (2023) — "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
- Jiang et al. (2023) — "LLMLingua: Compressing Prompts for Accelerated Inference"
- Schulhoff et al. (2024) — "HackAPrompt: A Large-Scale Benchmark for Prompt Injection"

### Provider Docs (Version-Pinned)
- OpenAI Structured Outputs: `https://platform.openai.com/docs/guides/structured-outputs` (v2024-10-01)
- Anthropic Tool Use: `https://docs.anthropic.com/en/docs/tool-use` (v2024-10-22)
- OpenAI Prompt Caching: `https://platform.openai.com/docs/guides/prompt-caching` (verified Nov 2024)

### Tools & Frameworks
- **DSPy:** `https://github.com/stanfordnlp/dspy` (Production-ready APO)
- **Langfuse Prompt Management:** `https://langfuse.com/docs/prompt-management`
- **Weights & Biases Prompts:** `https://docs.wandb.ai/guides/prompts`
- **LLMLingua-2:** `https://github.com/microsoft/LLMLingua`

### Cross-Chapter References
- Ch1: Grundlagen — JSON Mode Intro, LLM Basics
- Ch4: Token Management — Budgets, Truncation, Semantic Caching (Deep Home)
- Ch7: Evaluation — Golden Set Methodology, LLM-as-a-Judge, Statistical Rigor
- Ch11: Agents/Tools — ReAct Pattern → Agent Architectures
- Ch16: Security — Prompt Injection Deep Dive (Deep Home)
- Ch17: Inference Optimization — Prompt Caching → KV Cache, Speculative Decoding
- Ch19: Production — Prompt Versioning → Canary Deployments, Rollback, Cost Optimization

---

## Appendix A.3 — Temperature Behavior Reference (Model/Date Stamped)

| Model (Snapshot) | Temp 0.0 | Temp 0.3 | Temp 0.7 | Temp 1.0 | Notes |
|------------------|----------|----------|----------|----------|-------|
| gpt-4o-mini-2024-07-18 | Deterministisch* | Low Variance | Medium | High | *Server-side batching → nicht bit-identisch |
| gpt-4o-2024-08-06 | Deterministisch* | Low Variance | Medium | High | |
| claude-3-5-sonnet-20241022 | Deterministisch* | Low Variance | Medium | High | |
| **Stand:** November 2024. Verhalten kann sich mit Model Updates ändern. Immer Pinned Snapshots verwenden. |

---

## Changelog (Outline Version)

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-07-17 | Initial A+ Outline based on Research Report |

---

**Next Agent:** chapter-writer → writing-editor  
**Pipeline:** writing-researcher ✓ → outline-writer ✓ → chapter-writer → writing-editor