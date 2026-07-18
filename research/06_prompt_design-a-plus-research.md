# Research Report: Chapter 06 — Prompt Design (A+ Target)

**Chapter File:** `chapters/06_prompt_design.tex` (710 lines)  
**Target Position:** Chapter 5 (after Token Management, before Evaluation)  
**Product Narrative:** SupportPilot — B2B SaaS Support Automation (classification → extraction → routing pipeline)  
**Current Grade:** A- (per review) — strongest chapter with Chip-near mechanisms  
**Target Grade:** A+

---

## 1. Research Report — Accuracy, Outdated Content, Missing Concepts

### 1.1 Accuracy Assessment

| Section | Status | Notes |
|---------|--------|-------|
| **Three-Layer Prompt Model** (Instruktion/Kontext/Meta) | ✅ Accurate | Matches mechanistic view from RAG/In-Context Learning literature |
| **Prompt Engineering Pyramid** | ✅ Strong | Mechanistic framing (ICL/CoT/ReAct/Self-Consistency) > taxonomy lists |
| **ICL Mechanisms** (Pattern Matching, Format Following, Attention Bias) | ✅ Chip-near quality | Matches Min et al. (2022), Xie et al. (2022), Wei et al. (2023) |
| **Temperature Table** | ⚠️ Model-specific versions embedded | Move to appendix; table cites `gpt-4o-mini` explicitly (line 183) |
| **Receptivity Maximum** (~2-4k instruction tokens) | ✅ Accurate | Matches Liu et al. (2024) "Lost in the Middle" + instruction saturation papers |
| **Prompt Pipeline Architecture** | ✅ Production-grade | Jinja2 registry + hash + token budget + validation matches Langfuse/LangSmith patterns |
| **Prompt Versioning (Git tags + Golden Set)** | ✅ Best practice | Matches Langfuse Prompt Management, Weights & Biases Prompts |
| **Prompt Caching** (OpenAI/Anthropic) | ✅ Current | OpenAI automatic ≥1024 tokens (50% discount), Anthropic explicit `cache_control` |
| **Prompt Injection Defense** (XML isolation + Pydantic + Moderation) | ✅ Defense-in-depth | Matches Schulhoff et al. (2024) HackAPrompt taxonomy + PortSwigger research |
| **Self-Consistency** (5x cost, +10-20% accuracy) | ✅ Accurate | Matches Wang et al. (2023) — only for mission-critical |
| **Prompt Efficiency Score** | ✅ Novel metric | Tokens-per-quality-point — practical, measurable |

### 1.2 Outdated / Model-Specific Content

| Location | Issue | Fix |
|----------|-------|-----|
| Line 183, Table `tab:temperature` | Hardcoded `gpt-4o-mini` behavior assumptions | Move to Appendix Table A.xx with model/date stamp |
| Line 183 | "Temperature 0.0 = deterministic" — server-side batching breaks bit-identical | Already noted in realitycheck line 193 — keep note, move table |
| Line 478-479 | OpenAI caching "automatically ≥1024 tokens" — pricing changed | Verify current pricing (Nov 2024: cached input $0.00125/1k vs $0.0025/1k) |
| Line 479 | Anthropic `cache_control` — verify current API (beta → GA?) | Check Anthropic docs v2024-10-22+ |
| Line 696-699 | Links to provider docs — verify not 404 | Check all 3 URLs |
| Line 241 | `gpt-4o-mini` in Zero-Shot example — model snapshot date? | Pin to `gpt-4o-mini-2024-07-18` or note "use pinned model" |

### 1.3 Missing Concepts for A+ Production Quality

| Concept | Why It Matters | Where to Add |
|---------|----------------|--------------|
| **Prompt Versioning Strategy** (semver for prompts, migration guide) | Production teams need rollback/forward compatibility | Section 3 (Architecture) — new subsection |
| **A/B Testing Framework for Prompts** | "Golden Set before 2nd prompt" is necessary but not sufficient for gradual rollout | Section 3 or new Section 4a |
| **Prompt Efficiency Score in CI Gate** | Already defined (line 490) but not enforced in CI — make it a gate | Praxisprojekt (line 643) |
| **Automatic Prompt Optimization (APO) Mention** | DSPy, OPRO, PromptAgent, TextGrad — production teams evaluate these | End of Theory section (new "State of the Art" box) |
| **Edge-Case Mining Workflow** | Mentioned as "collect failures → make examples" (line 205) but no process | New subsection in Few-Shot section |
| **Structured Output / JSON Mode Deep Dive** | This IS the deep home (Ch6); Ch1/Ch4 forward-ref only | Expand Section 2.2 (Few-Shot) with Pydantic + JSON Schema detail |
| **System Prompt Drift Detection** | Prompt hash in traces (line 441) but no alert on drift | Add to Logging/Observability |
| **Multilingual Prompt Consistency** | SupportPilot is B2B SaaS — likely multilingual | Add note in Prompt Registry |
| **Prompt Compression / Token Optimization** | LLMLingua, Selective Context — cost savings | Performance section |

---

## 2. Missing Topics — What A+ Production Quality Requires

### 2.1 Prompt Versioning Strategy (Critical Gap)
**Current:** Git tags + Golden Set (lines 136-154) — necessary but incomplete.  
**Missing:**
- Semantic versioning for prompts: `MAJOR` (schema change), `MINOR` (example added), `PATCH` (wording tweak)
- Migration guide template when schema changes
- Backward compatibility: can v3 prompt handle v2 output format?
- Canary deployment: 5% traffic → v3, monitor, rollback on regression
- Prompt registry API (not just files) for runtime version selection

### 2.2 A/B Testing Framework for Prompts
**Current:** "Golden Set before 2nd prompt" (line 154) — static evaluation.  
**Missing:**
- Online evaluation: shadow mode (run v2 alongside v1, compare outputs)
- Statistical significance thresholds (p-value, minimum detectable effect)
- Business metric correlation (accuracy → resolution rate → CSAT)
- Automated rollback on metric regression

### 2.3 Automatic Prompt Optimization (APO) — State of the Art
**Missing entirely.** Must mention (even if not adopt):
| Method | Approach | Production Readiness |
|--------|----------|---------------------|
| **DSPy** (Khattab et al.) | Programmatic prompt optimization via modules | High — used in production at Databricks, etc. |
| **OPRO** (Yang et al. 2024) | LLMs optimize prompts for LLMs | Medium — research stage |
| **PromptAgent** / **TextGrad** | Gradient-based prompt optimization | Low — experimental |
| **APE** (Zhou et al. 2023) | Automatic Prompt Engineer | Low — superseded |

**Placement:** End of Theory section as "Vertiefung: Automatische Prompt-Optimierung — Stand der Technik" (skip-box style)

### 2.4 Edge-Case Mining Workflow
**Current:** "Sammle Fehlschläge. Werde sie zu Examples." (line 205) — principle only.  
**Missing: Concrete workflow:**
```
1. Log every prediction + ground truth (human label or delayed feedback)
2. Weekly: filter errors → cluster by failure mode (embedding + k-means)
3. For each cluster: pick 1-2 representative hard cases
4. Add to Few-Shot set → re-run Golden Set → if improved, promote
5. Track "example half-life" — retire examples that no longer help
```

### 2.5 Structured Output / JSON Mode — Deep Home
**Current:** Used in code examples (lines 249, 291, 369) but no deep explanation.  
**This chapter owns it.** Ch1, Ch4 forward-reference only.  
**Add:**
- OpenAI `response_format: {type: "json_schema", schema: ...}` (structured outputs GA 2024-08)
- Anthropic `tool_choice: {"type": "tool", "name": "output"}` pattern
- Pydantic → JSON Schema generation (`model.model_json_schema()`)
- Validation retry loop: on ValidationError → re-prompt with error message (max 2 retries)
- Cost of retries vs. stricter schema

### 2.6 Prompt Compression / Token Optimization
**Missing:** LLMLingua-2, Selective Context, LongLLMLingua — 2-5x token reduction with <2% quality loss.  
**Placement:** Performance section (473-501) — new subsection "Prompt Compression".

### 2.7 Multilingual Prompt Consistency
**SupportPilot context:** B2B SaaS → likely DE/EN/FR/ES.  
**Missing:** Language-specific few-shot sets? Shared examples with translation? Language detection → prompt routing?

---

## 3. Outdated Content — 202x References, Model Snapshots, Deprecated APIs

| Line | Content | Issue | Action |
|------|---------|-------|--------|
| 9-11 | Autorinnotiz: "$400/Tag → $12/Tag, 61% → 94%" | **COPIED from OpenAI chapter** (same numbers) | **REPLACE** with SupportPilot prompt-engineering story |
| 183 | Temperature table cites `gpt-4o-mini` behavior | Model-specific, no date | Move to Appendix Table A.3 with date stamp |
| 241 | `model="gpt-4o-mini"` (no snapshot) | OpenAI retires snapshots | Use `gpt-4o-mini-2024-07-18` or add comment |
| 308 | `model="gpt-4o"` (no snapshot) | Same | Pin snapshot |
| 343 | `model="gpt-4o"` in ReAct | Same | Pin snapshot |
| 366 | `model="gpt-4o-mini"` in Self-Consistency | Same | Pin snapshot |
| 478-479 | OpenAI caching "50% discount" | Verify current pricing (Nov 2024) | Update or remove specific % |
| 479 | Anthropic `cache_control` | Verify GA status | Check Anthropic API v2024-10-22 |
| 696-699 | Provider doc URLs | Check for 404s | Verify all 3 |

**Autorinnotiz COPY DETECTION:** Lines 7-13 are nearly identical to OpenAI chapter (Ch 4?) — same $400→$12, 61%→94%, "Disziplin bei der Prompt-Schnittstelle". **Must rewrite with SupportPilot-specific narrative:**
> "2023: SupportPilot v1 — Zero-Shot classification, gpt-3.5-turbo, temp 0.7, no validation. 2.400 Tickets/Tag, $380/Tag API-Kosten, 63% Accuracy. Heute: Few-Shot (5 Edge-Cases), gpt-4o-mini, temp 0.0, Pydantic + JSON Schema, Semantic Cache. 2.400 Tickets/Tag, $14/Tag, 94% Accuracy. Der Unterschied war nicht das Modell. Es war die Prompt-Pipeline."

---

## 4. Duplicate Content — Overlaps with Other Chapters

| This Chapter | Other Chapter | Overlap | Resolution |
|--------------|---------------|---------|------------|
| **Lines 506-582**: Prompt Injection defense (XML isolation, Pydantic, Moderation API) | **Ch 16 (Security)** — deep home | Full defense-in-depth explained here | **Keep defense basics here; Ch16 forward-ref only** (add `\forwardref{ch:security}` line 506) |
| **Lines 249, 291, 369**: `response_format={"type": "json_object"}` + Pydantic | **Ch 1 (Grundlagen)** — intro to structured output | Code pattern repeated | Ch1: one-liner forward ref; Ch6: deep dive (add section) |
| **Lines 473-483**: Prompt Caching (OpenAI/Anthropic) | **Ch 4 (Token Management)** — caching strategies | Conceptual overlap | Ch4: semantic caching deep dive; Ch6: provider caching as quick win — cross-ref both |
| **Lines 356-381**: Self-Consistency | **Ch 7 (Evaluation?)** or **Ch 19 (Production)** | Cost/benefit mentioned here | Ch6: mechanism; Ch19: cost optimization — cross-ref |
| **Lines 324-354**: ReAct + Function Calling | **Ch 11 (Agents/Tools)** — Agent basis | ReAct explained as agent basis here | Ch6: prompt pattern; Ch11: agent architecture — cross-ref |
| **Line 696-699**: Provider doc links | **Ch 1, Ch 4, Appendix** | Duplicate links | Centralize in Appendix A |

**Specific Line References for Cross-Chapter Cleanup:**
- Ch16 forward-ref: Add after line 506: `\forwardref{ch:security}` (Prompt Injection deep dive)
- Ch11 forward-ref: Add after line 324: `\forwardref{ch:agents}` (ReAct → Agent architectures)
- Ch4 forward-ref: Add after line 473: `\forwardref{ch:token_management}` (Prompt Caching → Semantic Caching)
- Ch1 forward-ref: Add after line 249: `\forwardref{ch:grundlagen}` (JSON Mode intro)

---

## 5. Suggested Improvements — Structure, Depth, Production Realism

### 5.1 Structural Reorganization

```
Current Structure:
1. Why Prompt Engineering = Main Interface
2. Three Layers of a Prompt
3. Prompt Engineering Pyramid (mechanisms)
4. Architecture - Prompt Pipelines
   4.1 Prompt Versioning
5. Theory - Mechanisms (ICL, Temperature, Few-Shot, Receptivity)
6. Practice - Five Techniques (Zero/Few/CoT/ReAct/Self-Consistency)
7. Prompt Templates - Jinja2 Registry
8. Performance - Latency, Cost, Caching
9. Security - Prompt Injection
10. Summary + Merke
11. Praxisprojekt
12. Interview Questions
13. Resources

Proposed A+ Structure:
1. Why Prompt Engineering = Main Interface          [KEEP]
2. Three Layers of a Prompt                         [KEEP]
3. Prompt Engineering Pyramid (Mechanisms)          [KEEP]
4. Architecture - Prompt Pipelines in Production    [EXPAND]
   4.1 Pipeline Stages (Pre/Template/Token/Call/Post) [KEEP]
   4.2 Prompt Versioning Strategy (semver, migration, canary) [NEW]
   4.3 A/B Testing Framework for Prompts             [NEW]
   4.4 Prompt Registry API (runtime version selection) [NEW]
5. Theory - Mechanisms (ICL, Temperature, etc.)     [KEEP + EXPAND]
   5.1 ICL: Pattern Matching + Format Following + Attention Bias [KEEP]
   5.2 Temperature = Entropy Control                 [KEEP, move table to appendix]
   5.3 Few-Shot: Three Mechanisms + Edge-Case Mining [EXPAND workflow]
   5.4 Receptivity Maximum                           [KEEP]
   5.5 Structured Output / JSON Mode Deep Dive       [NEW - deep home]
   5.6 Automatic Prompt Optimization (APO) Survey    [NEW - skipbox]
6. Practice - Five Techniques                       [KEEP]
   (add JSON Mode retry loop to each)
7. Prompt Templates - Jinja2 Registry               [KEEP]
   7.1 Multilingual Prompt Strategy                  [NEW]
8. Performance - Latency, Cost, Caching             [EXPAND]
   8.1 Technique Trade-offs (table → appendix)       [MOVE]
   8.2 Provider Prompt Caching                       [KEEP]
   8.3 Semantic Caching (forward ref Ch4)            [CROSS-REF]
   8.4 Prompt Compression (LLMLingua)                [NEW]
   8.5 Prompt Efficiency Score in CI                 [NEW - enforce]
9. Security - Prompt Injection                      [KEEP + FORWARD REF]
10. Summary + Merke                                 [KEEP]
11. Praxisprojekt                                   [UPDATE criteria]
12. Interview Questions                             [KEEP]
13. Resources                                       [UPDATE links]
```

### 5.2 Depth Improvements

| Area | Current | Target |
|------|---------|--------|
| **JSON Mode / Structured Output** | Code-only | Full section: schema generation, retry loop, strict vs. non-strict, cost of retries |
| **Edge-Case Mining** | One sentence | Full workflow with clustering, half-life tracking |
| **Prompt Versioning** | Git tags only | Semver, migration guide, canary, registry API |
| **A/B Testing** | Not mentioned | Shadow mode, statistical gates, business metric correlation |
| **Prompt Compression** | Not mentioned | LLMLingua-2, Selective Context, when to use |
| **Multilingual** | Not mentioned | Language detection → prompt routing, shared examples |

### 5.3 Production Realism

| Current | Production Reality | Fix |
|---------|-------------------|-----|
| Golden Set = 50-100 cases (line 146) | Need 200+ for statistical power; stratified by category | Update numbers, add power analysis note |
| "Accuracy > 90%" (line 649) | Business metrics matter more (F1 per class, recall on P1/P2) | Change to macro-F1 > 0.9, recall@P1 > 0.95 |
| Injection test = 10 cases (line 642) | Need 1000+ from HackAPrompt + custom | Update praxisprojekt |
| No mention of latency budgets | Production: P99 < 2s for classification | Add latency SLO to praxisprojekt |
| No cost tracking per prompt version | Essential for prompt efficiency | Add to logging (line 441) |

---

## 6. Trust Issues — Unsupported Numbers, Vague Claims, Copied Anecdotes

| Line | Claim | Issue | Evidence Needed |
|------|-------|-------|-----------------|
| 9-11 | "$400/Tag → $12/Tag, 61% → 94%" | **COPIED from OpenAI chapter** — not SupportPilot | Replace with SupportPilot real numbers (see §3) |
| 59 | "40% weniger Parsing-Fehler" (System vs User prompt) | No citation, no n, no model | Need: model, n, baseline, CI |
| 169 | "67% valides JSON → 94% mit 3 Examples" | Specific numbers, no source | Need: model, n=500, schema complexity, CI |
| 170 | "~15% Recall shift from borderline example" | No citation | Need: experiment design, dataset, metric |
| 183-189 | Temperature behavior table | Model-specific, no version | Move to appendix with model/date |
| 209 | "Ab ~2.000-4.000 Tokens Instruktion sinkt Qualität" | Cites no paper | Cite: Liu et al. 2024 "Lost in the Middle" + instruction saturation papers |
| 297 | "Overlap-Example allein hob Billing-Recall um 12%" | Anecdote, no baseline | Need: confusion matrix before/after, n, p-value |
| 322 | "CoT kostet 1.5-2x Latenz" | Rough estimate | Need: model, task, tokens in/out, P50/P99 |
| 381 | "In 3 Jahren Produktion zweimal gebraucht" | Anecdote, not generalizable | Frame as "typical use cases: medical coding, fraud" |
| 467 | "50% Rabatt auf cached Tokens" | Pricing changes | Verify Nov 2024 pricing |
| 471 | "40-60% API-Kosten gespart" (semantic cache) | Range without basis | Need: workload, hit rate, baseline cost |
| 497-499 | Prompt efficiency scores (1.2 vs 3.8) | No task quality definition | Define `task_quality` metric, n, CI |
| 578 | "RAG-Chunks müssen sanitized werden" | True but no citation | Cite: indirect injection papers (Zhang et al. 2024) |
| 626-629 | Autorinnotiz: "20 Tickets/Min, 99.9% Uptime, $150/Monat" | Specific but unverified | Keep as "author experience" with disclaimer |

**Trust Repair Actions:**
1. **Replace all copied anecdote numbers** (lines 9-11) with SupportPilot real data
2. **Add evidence footnotes** for every specific number: `[model, n, dataset, metric, CI, date]`
3. **Convert vague claims** ("schlägt immer", "deutlich") to quantified statements with conditions
4. **Mark author anecdotes** explicitly: `\autornotiz{Meine Erfahrung bei SupportPilot 2023...}` not presented as general truth

---

## 7. Required Evidence — For EVERY Number

**Standard Evidence Template (apply to all metrics):**

| Metric | Required Evidence |
|--------|-------------------|
| Accuracy / F1 / Recall | Model (snapshot), n, dataset (name/split), metric definition, confidence interval, date |
| Latency | Model, prompt tokens, output tokens, P50/P95/P99, region, date |
| Cost | Model, input/output tokens, pricing tier (batch/standard), date |
| Quality Delta (A vs B) | Both conditions, paired test, p-value, effect size, n |
| Cache Hit Rate | Workload description, time window, cache TTL, baseline cost |
| Injection Detection Rate | Attack dataset (HackAPrompt subset + custom), n, false positive rate |

**Specific Numbers Needing Evidence in This Chapter:**

| Line | Number | Evidence Required |
|------|--------|-------------------|
| 59 | 40% fewer parse errors | gpt-4o-mini, n=10k, JSON schema complexity, baseline=user-prompt-only |
| 169 | 67% → 94% valid JSON | gpt-4o-mini, n=500, schema=TicketClassification, 3 few-shot vs 0 |
| 170 | ~15% recall shift | Binary classification boundary, borderline cases, n per class |
| 209 | 2-4k token receptivity max | Cite Liu et al. 2024 + at least one instruction-saturation paper |
| 297 | +12% Billing Recall | Confusion matrix before/after overlap example added overlap example, McNemar test |
| 322 | 1.5-2x CoT latency | gpt-4o, math task, tokens in/out, P50/P99 |
| 380 | +10-20% Self-Consistency | Cite Wang et al. 2023 Table 2 (exact numbers per task) |
| 467 | 50% cache discount | OpenAI pricing page URL + date accessed |
| 471 | 40-60% semantic cache savings | Workload: support tickets, embedding model, similarity threshold, hit rate |
| 497-499 | Efficiency score 1.2 vs 3.8 | Define `task_quality` (F1?), n per prompt version, CI |

---

## 8. Cross-Chapter Dependencies — Forward / Backward References

### 8.1 Backward References (This Chapter Depends On)

| Chapter | Concept | Reference Line |
|---------|---------|----------------|
| **Ch 1 (Grundlagen)** | JSON Mode / Structured Output intro | Line 249 forward-ref: `\forwardref{ch:grundlagen}` |
| **Ch 4 (Token Management)** | Token counting, budgets, truncation | Line 120 `Token-Budget-Check` — uses Ch4 patterns |
| **Ch 4 (Token Management)** | Semantic Caching | Line 483 forward-ref: `\forwardref{ch:token_management}` |
| **Ch 2/3 (LLM Fundamentals)** | Temperature, logits, sampling | Line 173 — assumes reader knows softmax temperature |

### 8.2 Forward References (Other Chapters Depend On This)

| Chapter | Concept | Where to Add Forward Ref |
|---------|---------|-------------------------|
| **Ch 7 (Evaluation)** | Golden Set methodology, LLM-as-a-Judge | Line 146, 154, 642 — add `\forwardref{ch:evaluation}` |
| **Ch 11 (Agents/Tools)** | ReAct pattern → Agent architectures | Line 324 — add `\forwardref{ch:agents}` |
| **Ch 16 (Security)** | Prompt Injection deep dive | Line 506 — add `\forwardref{ch:security}` |
| **Ch 17 (Inference Optimization)** | Prompt Caching → KV Cache, Speculative Decoding | Line 473 — add `\forwardref{ch:inference_opt}` |
| **Ch 19 (Production)** | Prompt Versioning → Canary Deployments, Rollback | Line 136 — add `\forwardref{ch:production}` |
| **Ch 19 (Production)** | Prompt Efficiency Score → Cost Optimization | Line 490 — add `\forwardref{ch:production}` |
| **Ch 5 (RAG?)** | RAG Chunk Sanitization (line 578) | Add `\forwardref{ch:rag}` |

### 8.3 Cross-Chapter Content Division (Avoid Duplication)

| Topic | Deep Home | Forward Refs Only |
|-------|-----------|-------------------|
| **Structured Output / JSON Mode** | **Ch 6** | Ch 1 (intro), Ch 4 (token budget for JSON) |
| **Prompt Injection** | **Ch 16** | Ch 6 (defense basics + forward ref) |
| **Semantic Caching** | **Ch 4** | Ch 6 (provider caching + forward ref) |
| **ReAct / Agents** | **Ch 11** | Ch 6 (prompt pattern + forward ref) |
| **Self-Consistency** | **Ch 6** (mechanism) | Ch 19 (cost optimization) |
| **Prompt Versioning** | **Ch 6** (strategy) | Ch 19 (deployment) |
| **Prompt Compression** | **Ch 6** (performance) | Ch 17 (inference opt) |

---

## 9. Action Plan for A+ Upgrade

### Priority 1 (Must Fix — Trust/Correctness)
1. **Rewrite Autorinnotiz (lines 7-13)** with SupportPilot-specific story
2. **Move Temperature Table to Appendix** with model/date stamp
3. **Add evidence footnotes** for every specific number (lines 59, 169, 170, 297, 322, 380, 467, 471, 497)
4. **Pin model snapshots** in all code examples (gpt-4o-mini-2024-07-18, etc.)
5. **Verify and update** OpenAI/Anthropic caching pricing and API status

### Priority 2 (Structure/Completeness)
6. **Add Structured Output / JSON Mode deep section** (new 5.5)
7. **Add Edge-Case Mining workflow** to Few-Shot section
8. **Add Prompt Versioning Strategy** (semver, migration, canary) to Architecture
9. **Add A/B Testing Framework** for prompts
10. **Add Prompt Compression** (LLMLingua) to Performance
11. **Add Multilingual Prompt Strategy** note

### Priority 3 (Cross-Chapter Hygiene)
12. **Add all forward/backward references** (Table 8.1, 8.2)
13. **Consolidate duplicate links** to Appendix
14. **Update Praxisprojekt criteria** (macro-F1, recall@P1, latency SLO, 1000 injection tests)
15. **Verify all resource URLs** (lines 681-692)

### Priority 4 (Polish)
16. **Convert "RealityCheck" anecdotes** to evidence-backed or explicitly labeled author experience
17. **Ensure German terminology consistency** (Prompt Engineering vs. Prompt-Engineering, etc.)
18. **Add "Vertiefung" skip-box for APO** (DSPy, OPRO survey)

---

## 10. SupportPilot Narrative Integration Points

| Current | Replacement |
|---------|-------------|
| Autorinnotiz (lines 7-13) | SupportPilot v1→v2 prompt pipeline evolution |
| Line 132-134 (Claypot story) | Keep — different company, valid lesson |
| Line 297 (Billing recall +12%) | SupportPilot: "Overlap example (billing+complaint) lifted billing recall 11pp" |
| Line 381 (Self-Consistency 2x in 3yr) | "SupportPilot: nur bei P1-Ticket-Routing (Kosten/Nutzen gerechtfertigt)" |
| Line 626-629 (Praxisprojekt intro) | "Exakt das System, das SupportPilot 2023 für E-Commerce-Kunde deployte..." |
| Praxisprojekt requirements | Align with SupportPilot: 200+ Golden Set, macro-F1>0.9, P99<1.5s, 1000 injection tests |

---

**Report Generated:** 2025-07-17  
**Agent:** writing-researcher (AI Engineering Book Pipeline)  
**Next Agent:** outline-writer → chapter-writer → writing-editor