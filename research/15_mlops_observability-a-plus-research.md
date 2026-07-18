# Research Report: Chapter 15 — MLOps und Observability (A+ Target)

**Chapter File:** `chapters/15_mlops_observability.tex`
**Current Grade:** C- (~1,200 words, thin, Autornotiz copied from RAG chapter, observability overlaps Ch9/10)
**Target Grade:** A+ (~3,000 words, production-real, SupportPilot narrative arc)
**Quality Bar:** Chip Huyen / Martin Kleppmann / Alex Xu

---

## 1. Research Report — Accuracy, Outdated Content, Missing Concepts

### Accuracy Assessment

| Section | Status | Issues |
|---------|--------|--------|
| Autornotiz (L7-12) | **Copied verbatim from RAG chapter** | Same gpt-4o-mini 2024-07-18 incident appears in Ch13 (RAG). Must be NEW SupportPilot story. |
| Was macht MLOps anders? (L26-34) | Accurate but shallow | Three points correct but no depth. Missing: eval-driven dev loop, probabilistic testing, cost as first-class metric. |
| LLMOps-Lebenszyklus (L39-60) | Correct structure | Five phases ok but each gets 1 bullet. No tooling, no decision criteria, no failure modes per phase. |
| Versionierung (L65-98) | Good skeleton, thin meat | Prompts-as-code: no Jinja2+Git tags+eval-results pattern. Data versioning: mentions DVC/LakeFS but no code. Model Cards: listed but no template/example. |
| CI/CD (L103-151) | Pipeline sketch only | GitHub Actions example is generic. Missing: Golden Set gate, cost gate, canary metrics gate, LLM-judge in CI, schema validation details. |
| Monitoring (L156-180) | **Major overlap with Ch9/Ch14** | Quality drift, data drift, cost drift, perf drift — all mentioned in Ch9 (eval metrics) and Ch14 (ops metrics). No SLO/SLI definitions, no alert routing, no drift detection algorithms (KS-test, PSI, embedding drift). |
| Governance (L184-204) | Roles listed, no workflow | Model Owner/Data Steward/PO/Security Owner — names only. No RACI, no approval gates mechanics, no audit log implementation. |
| Prompt-Versionierung (L209-259) | Best section, still incomplete | Jinja2 folder structure good. Test example trivial (keyword matching). Missing: A/B test framework, eval results stored WITH version, semantic diff, canary promotion criteria. |
| Kostenmanagement (L263-324) | Decent, numbers unbacked | 80% soft alert, hard cap, per-customer limit — all asserted without evidence. Cost tracker code is toy. Missing: anomaly detection (2x baseline), token accounting per feature, chargeback model. |
| Incident Response (L329-361) | Runbook skeleton | 5-step runbook generic. Missing: concrete runbooks for Quality Drop / Cost Spike / Provider Outage with SLAs, escalation paths, PagerDuty/Slack routing, post-mortem template. |
| Praxisprojekt (L381-396) | Good exercise, vague success criteria | "Alerts feuern bei injizierten Anomalien innerhalb von 2 Minuten" — 2 min from where? No baseline. |

### Outdated / Version-Specific Content

| Line | Content | Issue |
|------|---------|-------|
| L8-10 | `gpt-4o-mini-2024-07-18` | Model snapshot from 2024. Book targets 2026+. Use generic "model pinning to specific snapshot" pattern. |
| L121-149 | `actions/checkout@v4` | GitHub Actions version. Pin to major or use generic "checkout action". |
| L404-406 | MLflow, Langfuse, Evidently AI | Tool references ok but no version. Langfuse v2/v3 breaking changes possible. |
| L391 | `Quality < 0.7`, `Cost/Query > 0.02 EUR`, `P95 > 3s` | Arbitrary thresholds. No justification, no dataset, no baseline. |

### Missing Concepts for A+ Production Quality

1. **SLO/SLI/SLA Definitions** — No formal service level objectives. Ch14 (ops) should define infra SLOs; Ch15 defines *model quality* SLOs (hallucination rate < 2%, factual accuracy > 90%, coherence > 0.85).
2. **Drift Detection Algorithms** — KS-test for numeric distributions, PSI (Population Stability Index) for categorical, embedding drift (cosine similarity shift), concept drift (label distribution shift). Currently: "Gemessen durch Stichproben" — handwavy.
3. **Prompt A/B Testing Framework** — Statistical significance, minimum sample size, guardrail metrics, automatic promotion/rollback.
4. **Feedback Loop (Human-in-the-Loop → Golden Set)** — Thumbs up/down → annotation queue → Golden Set expansion → eval re-run → canary promotion.
4. **Data Versioning Implementation** — DVC/LakeFS code examples, schema evolution handling, reproducibility.
5. **Model Cards with Teeth** — Not just documentation: enforceable constraints (max latency, max cost, min quality), auto-validated in CI.
6. **Cost Anomaly Detection** — Statistical (2x rolling 7-day baseline), attribution (which prompt/feature/user), auto-mitigation (circuit breaker to cheaper model).
7. **Alert Routing & On-Call** — PagerDuty/Slack/Opsgenie integration, severity tiers (SEV1/2/3), runbook links in alert.
8. **Multi-Provider Fallback Automation** — Not just "switch to Anthropic": latency budget, quality parity check, cost delta, automatic failback.
9. **Evaluation-Driven Development Loop** — Ch9 eval system feeds Ch15 CI gate; Ch15 production metrics feed Ch9 Golden Set refresh.
10. **SupportPilot Narrative Arc** — v1 (no monitoring) → v2 (Langfuse tracing) → v3 (SLOs + alerts) → v4 (prompt drift auto-rollback). Current Autornotiz is a copy-paste from RAG chapter.

---

## 2. Missing Topics — Required for A+ Production Quality

| Topic | Why Critical | Where to Place |
|-------|--------------|----------------|
| **SLO/SLI Definitions for LLM Quality** | Without SLOs, "quality drift" is undefinable. Ch14 has infra SLOs; this chapter needs *model* SLOs. | New section after Monitoring (before Governance) |
| **Drift Detection: KS-Test, PSI, Embedding Drift** | "Stichproben" is not engineering. Need code + thresholds + automation. | Expand Monitoring section (L156-180) |
| **Prompt A/B Testing Framework** | Production prompt changes need statistical rigor, not vibes. | New subsection in Prompt-Versionierung |
| **Feedback Loop: Human Signals → Golden Set** | Closes the loop. Ch9 creates Golden Set; Ch15 expands it from production. | New section after Prompt-Versionierung |
| **Data Versioning with DVC/LakeFS (Code)** | "DVC/LakeFS mentioned" ≠ usable. Need `dvc add`, `dvc push`, schema check CI step. | Expand Datenversionierung (L79-87) |
| **Model Cards as Enforceable Contracts** | Model Card = documentation + CI-validated constraints. | Expand Modelldokumentation (L89-98) |
| **Cost Anomaly Detection (Statistical)** | 80% budget alert is reactive. Need proactive: "cost/query 2x baseline → alert → auto-circuit-breaker". | Expand Kostenmanagement (L263-324) |
| **Alert Routing: PagerDuty/Slack + Runbook Links** | Alert without runbook link = wasted time. | New subsection in Alerting (L170-179) |
| **Multi-Provider Fallback with Quality Parity Check** | Fallback that degrades quality silently is worse than outage. | Expand Fallback-Strategien (L355-361) |
| **Incident Runbooks (Concrete, 3 Types)** | Generic 5-step runbook useless at 3am. Need: Quality Drop, Cost Spike, Provider Outage — each with detection query, mitigation commands, escalation, post-mortem template. | Replace Incident Response section (L329-361) |
| **SupportPilot v1→v4 Narrative** | Replaces copied Autornotiz. Shows evolution, not just end state. | New Autornotiz + woven through chapter |
| **Evaluation-Driven Dev Loop (Ch9 ↔ Ch15)** | Golden Set created in Ch9, gate in Ch15 CI, production metrics refresh Golden Set. | Cross-refs throughout + new subsection |
| **Prompt Semantic Diff + Eval Results Stored with Version** | Git diff shows text change; need *semantic* change + quality delta. | Prompt-Versionierung section |

---

## 3. Outdated Content — 202x Refs, Model Snapshots, Deprecated APIs

| Location | Content | Fix |
|----------|---------|-----|
| L8-10 | `gpt-4o-mini-2024-07-18` — specific 2024 snapshot | Replace with pattern: `model_pin: "provider/model@snapshot-date"` — explain *why* pinning matters, not which snapshot |
| L121-149 | `actions/checkout@v4` | Use `actions/checkout@v4` is fine but note: pin to SHA in production. Add comment. |
| L391 | Hardcoded thresholds: `Quality < 0.7`, `Cost/Query > 0.02 EUR`, `P95 > 3s` | Remove numbers or mark as "Beispielwerte — anpassen an dein SLO". Better: derive from Ch9 eval baseline. |
| L404-406 | Tool list without versions | Add "Stand 2025" or link to version-pinned docs. |
| L18 | "2026" not in text but roadmap.sh AI Engineer roadmap is 2026 — book should be timeless. | No year references in body text (AGENTS.md: "Timeless — no year references"). |

---

## 4. Duplicate Content — Overlaps with Other Chapters

| This Chapter (Ch15) | Overlaps With | Specific Lines | Resolution |
|---------------------|---------------|----------------|------------|
| Quality drift, data drift, cost drift, perf drift (L162-168) | **Ch9 (Evaluation)** — quality metrics, Golden Set | Ch9 L40-60: hallucination rate, factual accuracy, coherence | Ch9 = *how to measure* (eval methodology). Ch15 = *production monitoring* (continuous, automated, alerting). Cross-ref explicitly. |
| Latenz, Fehlerquoten, Timeouts (L167) | **Ch14 (Deployment/Operations)** — infra metrics | Ch14 likely has P50/P95 latency, error rate, availability | Ch14 = *infrastructure* SLOs. Ch15 = *model quality* SLOs. Separate concerns. |
| Cost tracking (L263-324) | **Ch10 (Provider/Deployment)** — provider costs | Ch10 likely covers provider pricing, routing | Ch10 = *provider selection/cost*. Ch15 = *budget enforcement, anomaly detection, chargeback*. |
| Provider outage fallback (L340, L358-360) | **Ch10 (Deployment)** — multi-provider routing | Ch10 probably has Semantic Router pattern | Ch10 = *routing logic*. Ch15 = *fallback automation, circuit breaker, failback criteria*. |
| Golden Dataset tests in CI (L112, L135) | **Ch9 (Evaluation)** — Golden Set creation | Ch9 defines Golden Set | Ch9 = *build Golden Set*. Ch15 = *Golden Set as CI gate + production refresh loop*. |
| Prompt versioning (L209-259) | **Ch6 (Prompt Engineering)** — prompt structure | Ch6 likely covers Jinja2, few-shot, CoT | Ch6 = *prompt design patterns*. Ch15 = *prompt lifecycle: version, test, deploy, rollback, A/B test*. |
| Model Cards (L89-98) | **Ch9/Ch13** — model evaluation docs | Ch9 eval results, Ch13 RAG model selection | Ch15 = *Model Card as deployable artifact with enforceable constraints*. |

**Action:** Every overlap needs explicit cross-reference: `\cref{chap:evaluation}` / `\cref{chap:deployment}` / `\cref{chap:prompt_engineering}` with one-sentence "see ChX for...".

---

## 5. Suggested Improvements — Structure, Depth, Production Realism

### Restructured Chapter Outline (Target ~3,000 words)

```
15. MLOps und der Modell-Lebenszyklus
│
├─ Autornotiz: SupportPilot v1→v4 Evolution (NEW, replaces copied RAG story)
│
├─ 15.1 Motivation — Why MLOps ≠ DevOps (expand: probabilistic, external deps, drift, cost)
│
├─ 15.2 Der LLMOps-Lebenszyklus — 5 Phasen mit Decision Gates (expand each phase: entry/exit criteria, tools, failure modes)
│
├─ 15.3 Versionierung als Fundament
│   ├─ 15.3.1 Prompts als Code: Jinja2 + Git Tags + Eval Results Stored with Version
│   ├─ 15.3.2 Semantic Prompt Diff + Quality Delta (NEW)
│   ├─ 15.3.3 Datenversionierung: DVC/LakeFS + Schema Checks in CI (code examples)
│   ├─ 15.3.4 Model Cards als Deployable Contracts (NEW: enforceable constraints)
│
├─ 15.4 CI/CD für LLM-Systeme — Pipeline mit Gates
│   ├─ 15.4.1 Golden Set Gate (from Ch9) — pass/fail + quality delta threshold
│   ├─ 15.4.2 Cost Gate — token budget per test suite + anomaly vs baseline
│   ├─ 15.4.3 Canary Metrics Gate — quality SLO + cost SLO + latency SLO (NEW)
│   ├─ 15.4.4 LLM-Judge in CI — semantic eval, not keyword (code)
│   ├─ 15.4.5 GitHub Actions / GitLab CI Template (production-ready)
│
├─ 15.5 Monitoring & Drift-Erkennung — Production Observability
│   ├─ 15.5.1 SLO/SLI Definitions für LLM-Qualität (NEW: hallucination<2%, factual>90%, coherence>0.85)
│   ├─ 15.5.2 Drift Detection Algorithms: KS-Test, PSI, Embedding Drift, Concept Drift (code + thresholds)
│   ├─ 15.5.3 Cost Anomaly Detection: 2x Rolling Baseline + Attribution (NEW)
│   ├─ 15.5.4 Alert Routing: PagerDuty/Slack + Runbook Links + Severity Tiers (NEW)
│   ├─ 15.5.5 Tracing: Langfuse/Helicone Integration — Request→Response→Feedback (NEW)
│
├─ 15.6 Prompt-Versionierung in der Praxis (expand existing)
│   ├─ 15.6.1 A/B Test Framework: Statistical Significance + Guardrails + Auto-Promote (NEW)
│   ├─ 15.6.2 Feedback Loop: Thumbs Up/Down → Annotation Queue → Golden Set Refresh (NEW)
│
├─ 15.7 Kostenmanagement — Budget als First-Class Constraint
│   ├─ 15.7.1 Token Accounting per Feature / User / Prompt Version
│   ├─ 15.7.2 Proactive Anomaly Detection (not just 80% budget alert)
│   ├─ 15.7.3 Chargeback Model for B2B SaaS (SupportPilot context)
│
├─ 15.8 Incident Response — Conkrete Runbooks (replace generic)
│   ├─ 15.8.1 Runbook: Quality Drop (Detection: SLO breach → Mitigation: auto-rollback to last passing prompt)
│   ├─ 15.8.2 Runbook: Cost Spike (Detection: 2x baseline → Mitigation: circuit breaker → cheaper model)
│   ├─ 15.8.3 Runbook: Provider Outage (Detection: error rate > 5% → Mitigation: multi-provider failover with quality parity)
│   ├─ 15.8.4 Post-Mortem Template + Runbook Update Process
│
├─ 15.9 Governance & Compliance (expand roles → RACI + audit log implementation)
│
├─ Zusammenfassung
├─ Merke: "MLOps = Eval-Driven Dev Loop + Production SLOs + Automated Drift Response"
├─ Praxisprojekt (enhance: add drift injection, cost anomaly injection, A/B test)
└─ Ressourcen
```

### Depth Increases Per Section

| Section | Current | Target | Delta |
|---------|---------|--------|-------|
| Autornotiz | 5 lines (copied) | 15 lines (SupportPilot v1→v4) | +200% |
| Lebenszyklus | 12 lines | 40 lines (decision gates per phase) | +230% |
| Versionierung | 34 lines | 100 lines (semantic diff, DVC code, Model Card contract) | +190% |
| CI/CD | 48 lines | 120 lines (4 gates, LLM-judge, production template) | +150% |
| Monitoring | 24 lines | 150 lines (SLOs, 4 drift algos, cost anomaly, alert routing, tracing) | +525% |
| Prompt-Versionierung | 50 lines | 100 lines (A/B framework, feedback loop) | +100% |
| Kosten | 61 lines | 80 lines (token accounting, chargeback, proactive detection) | +30% |
| Incident Response | 33 lines | 120 lines (3 concrete runbooks + post-mortem) | +260% |
| Governance | 20 lines | 40 lines (RACI, audit log impl) | +100% |

---

## 6. Trust Issues — Unsupported Numbers, Vague Claims, Copied Anecdotes

| Claim | Location | Problem | Required Evidence |
|-------|----------|---------|-------------------|
| "Halluzinationsrate 8% → 23% innerhalb 2h" | L8-9 (Autornotiz) | **Copied from RAG chapter**. No dataset, no n, no baseline, no scope. | NEW SupportPilot incident with real metrics. |
| "80% des Budgets erreicht" → Alert | L285, L306 | Arbitrary threshold. Why 80%? Why not 70% or 90%? | Evidence: "80% gives 3-5 day reaction window at typical burn rate" + citation. |
| "2 Minuten" Alert-Feuerzeit | L396 | From what trigger? Injected anomaly how? No baseline. | Define: "P99 detection latency from metric emission to PagerDuty alert = 2 min" + measurement method. |
| "Quality < 0.7" | L391 | What metric? Hallucination rate? Factual accuracy? Composite? On what dataset? | Define SLI: "Composite quality score (0.4×factual + 0.3×coherence + 0.3×relevance) on Golden Set v3, n=500". |
| "Cost/Query > 0.02 EUR" | L391 | Which model? GPT-4o? GPT-4o-mini? Includes caching? | "GPT-4o-mini, 1k input + 500 output tokens avg, no cache, 2025 pricing". |
| "P95 > 3s" | L391 | API only or E2E? Includes streaming first-token? | "E2E P95 including first token, measured at load balancer". |
| "Signifikante Kostenabweichung" | L175 | No definition. 10%? 2x? Statistical? | "Cost/query > 2x rolling 7-day median, p<0.01 (Mann-Whitney U)". |
| "Spürbare Qualitätsverschlechterung" | L176 | No threshold. | "Composite quality score drop > 5pp vs 7-day rolling avg, n≥100 samples". |
| "Datenanomalien bei Eingabeverteilungen" | L177 | How measured? | "PSI > 0.2 on input embedding clusters OR KS-test p<0.001 on token length distribution". |
| "Multi-Provider Fallback" | L358 | Quality parity? Latency budget? Cost delta? | "Failover only if: quality_delta < 3pp AND latency_p95 < 1.5x primary AND cost_delta < 2x". |
| "Prompt Caching: wiederkehrende Prefix-Tokens gecached" | L318 | Which providers? What prefix length? Savings? | "OpenAI: ≥1024 tokens prefix, 50% input cost reduction. Anthropic: ≥2048 tokens, 90% reduction. Measured on SupportPilot system prompt (1.8k tokens)". |

---

## 7. Required Evidence — For EVERY Number

**Template for each metric in chapter:**
```
Metric: <name>
Baseline: <value> (measured on <dataset>, n=<N>, date=<YYYY-MM>)
Current: <value> (measured on <dataset>, n=<N>, date=<YYYY-MM>)
Delta: <absolute> / <relative>
Scope: <which model, which prompt version, which feature, which tenant tier>
What Changed: <prompt v2→v3, model snapshot upgrade, traffic pattern shift>
Limitations: <sample bias, evaluation method constraints, time window>
Source: <eval run ID, monitoring dashboard URL, incident report>
```

### Numbers Requiring Evidence in This Chapter

| Number | Context | Evidence Needed |
|--------|---------|-----------------|
| 80% budget alert threshold | L285, L306 | Why 80%? Reaction window analysis. |
| 2x baseline cost anomaly | Implied in L175, L317 | Statistical basis, false positive rate. |
| 2 min canary detection | L396 | Measurement: metric emission → alert receipt. |
| 99.95% availability | Not yet but implied by SLOs | Definition: infra vs model availability. |
| Quality < 0.7 | L391 | SLI definition, dataset, n. |
| Cost/Query > 0.02 EUR | L391 | Model, token breakdown, pricing date. |
| P95 > 3s | L391 | E2E vs API, percentile method, load level. |
| 5% drift threshold (Autornotiz) | L10 | Why 5%? False positive/negative analysis. |
| 5% traffic canary | L10, L147 | Why 5%? Statistical power calculation. |
| PSI > 0.2 / KS-test p<0.001 | Proposed | Threshold calibration on historical data. |
| Embedding drift cosine < 0.85 | Proposed | Calibration on production traffic. |
| Quality SLO: hallucination < 2% | Proposed | Measurement method (LLM-judge? Human?), n, confidence interval. |

---

## 8. Cross-Chapter Dependencies — Forward/Backward References

### Backward References (This Chapter Must Reference)

| Chapter | Topic | Reference Style |
|---------|-------|-----------------|
| **Ch6 (Prompt Engineering)** | Jinja2 templates, few-shot, CoT, prompt structure | `\cref{chap:prompt_engineering}` — "Prompt-Design-Patterns siehe Kap. 6" |
| **Ch9 (Evaluation)** | Golden Set creation, quality metrics (hallucination, factual, coherence), LLM-judge | `\cref{chap:evaluation}` — "Golden Set Aufbau & Qualitätsmetriken: Kap. 9" |
| **Ch10 (Deployment/Provider)** | Multi-provider routing, Semantic Router, provider pricing, circuit breaker | `\cref{chap:deployment}` — "Provider-Routing & Circuit Breaker: Kap. 10" |
| **Ch14 (Operations/Observability)** | Infra SLOs (latency, error rate, availability), Prometheus/Grafana, alert routing | `\cref{chap:operations}` — "Infrastruktur-SLOs & Alert-Routing: Kap. 14" |

**Integration Points:**
- Ch9 Golden Set → Ch15 CI Gate (Golden Set Gate)
- Ch9 Eval Results → Ch15 Model Card (Performance Metrics)
- Ch10 Provider Failover → Ch15 Incident Runbook (Provider Outage)
- Ch14 Infra Metrics → Ch15 Combined Dashboard (infra + model quality)
- Ch14 Alert Routing → Ch15 Alert Routing (reuse PagerDuty/Slack config)

### Forward References (This Chapter Sets Up)

| Chapter | Topic | Setup in Ch15 |
|---------|-------|---------------|
| **Ch16 (Security — next chapter)** | Input/Output Guards, PII Masking, Injection Defense, Agent Tool Whitelist, HITL | Ch15 Incident Runbook "Security Incident" references Ch16 patterns. Ch15 Governance "Security Owner" role defined here, detailed in Ch16. |
| **Ch17 (Inference Optimization)** | Caching, quantization, speculative decoding | Ch15 Cost Management "Prompt Caching" / "Output Limits" → Ch17 implements. |
| **Ch18 (Model Customization)** | Fine-tuning, distillation, LoRA | Ch15 Model Versioning / Model Card → Ch18 produces new model versions. |
| **Ch19 (Caching/Routing/Guardrails)** | Semantic caching, router, guardrails | Ch15 Fallback Strategies / Cost Optimization → Ch19 builds infrastructure. |

### Cross-Reference Implementation

Add to chapter preamble:
```latex
% Cross-refs defined in main.tex
% \cref{chap:prompt_engineering}, \cref{chap:evaluation}, \cref{chap:deployment}, 
% \cref{chap:operations}, \cref{chap:security}, \cref{chap:inference_opt}, 
% \cref{chap:model_customization}, \cref{chap:caching_routing}
```

Every overlap section gets one-line cross-ref:
```latex
\textbf{Qualitätsmetriken} (Halluzinationsrate, Factual Accuracy, Coherence) 
werden in \cref{chap:evaluation} definiert. Hier nutzen wir sie als SLOs.
```

---

## Appendix: SupportPilot Narrative Arc (Replaces Copied Autornotiz)

### v1 — "Just Ship It" (Month 1)
- No monitoring. Deploy prompt changes directly to prod.
- Incident: Prompt update → 40% user complaints. No detection. Rollback manual, 4h downtime.
- Lesson: **Blind deployment = blind failure.**

### v2 — "Langfuse Tracing" (Month 3)
- Added: Request/response tracing, latency, token count, user feedback (thumbs).
- Detected: Cost creep (+15%/week) via token dashboard.
- Missed: Quality drift (hallucination 8%→18% over 2 weeks) — no quality SLO, no automated eval.
- Lesson: **Infra observability ≠ model observability.**

### v3 — "SLOs + Alerts" (Month 6)
- Defined: Quality SLO (composite < 0.15 hallucination, > 0.85 factual), Cost SLO (€0.015/query), Latency SLO (P95 < 2.5s).
- Alerting: PagerDuty SEV2 on SLO breach, runbook links.
- Incident: Provider silent model upgrade (gpt-4o-mini snapshot) → quality SLO breach → alert → auto-rollback to pinned model in 3 min.
- Lesson: **Model pinning + SLOs + auto-rollback = survival.**

### v4 — "Prompt Drift Auto-Rollback" (Month 10, Current)
- Added: Prompt A/B framework (statistical significance, guardrails), Feedback Loop (thumbs → annotation queue → Golden Set refresh weekly), Embedding drift detection (PSI on input clusters), Cost anomaly (2x baseline → circuit breaker to cheaper model).
- Incident: Gradual prompt drift (user language shift) → embedding drift PSI 0.31 → auto-canary of prompt v12 → quality SLO held → auto-promote.
- Zero manual interventions in 60 days.
- Lesson: **Closed loop: production signals → Golden Set → eval → canary → promote.**

---

## Research Complete — Ready for Outline Writer

**Next Agent:** `outline-writer` — receives this research report, produces detailed chapter outline with section word counts, code examples needed, cross-ref map, and SupportPilot narrative integration points.

**Key Deliverables for Outline Writer:**
1. Restructured outline (above) with word budgets per section
2. 12 code examples needed (DVC, KS-test, PSI, A/B test, cost anomaly, 3 runbooks, etc.)
3. Cross-reference table (8 refs)
4. SupportPilot v1→v4 narrative beats per section
5. Evidence requirements for 15+ numbers
6. Duplicate content resolution map (6 overlaps)