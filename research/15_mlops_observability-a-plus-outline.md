# Chapter 15 — MLOps und Observability: A+ Outline

**Target:** ~3,000 words | **Current:** ~1,200 words (C-) | **Quality Bar:** Chip Huyen / Kleppmann / Alex Xu
**Chapter File:** `chapters/15_mlops_observability.tex`
**Position:** Chapter 15 (nach Deployment/Ch14, vor Security/Ch16)
**Continuous Product:** SupportPilot (B2B SaaS Support-Automation)

---

## 13-Section Skeleton Mapping

| Required Section | Maps to Research Restructure | Word Budget |
|------------------|------------------------------|-------------|
| 1. Why this matters | 15.1 Motivation | 250 |
| 2. Mental Model | 15.2 LLMOps-Lebenszyklus (Decision Gates view) | 350 |
| 3. Architecture | 15.3 Versionierung + 15.4 CI/CD Gates | 400 |
| 4. Core Concepts | 15.5 Monitoring/SLOs/Drift + 15.7 Kosten | 500 |
| 5. Production Example | NEW: SupportPilot v1→v4 narrative arc (Autornotiz + woven) | 400 |
| 6. Trade-offs | 15.6 Prompt A/B + 15.7 Cost vs Quality | 300 |
| 7. Failure Modes | 15.8 Incident Runbooks (3 types) | 400 |
| 8. Evaluation | 15.4 Golden Set Gate + 15.5 Drift Algos | 300 |
| 9. Best Practices | 15.3 Model Cards + 15.5 Alert Routing + 15.9 Governance | 250 |
| 10. Anti-Patterns | From research gaps (copied Autornotiz, handwavy thresholds) | 200 |
| 11. Production Checklist | NEW: Deploy-ready checklist | 200 |
| 12. Exercises | Enhanced Praxisprojekt | 150 |
| 13. Further Reading | Curated with rationale | 100 |

**Total:** ~3,800 words (allows trimming to 3,000)

---

## Section-by-Section Detail

---

### 1. Why this matters (250 words)

**Core Argument:** MLOps ≠ DevOps. Three fundamental differences:
- **Probabilistic outputs** — same input → different output; quality must be measured continuously, not once at deploy
- **External dependencies you don't control** — model providers change snapshots, pricing, availability without notice
- **Drift is inevitable** — input distribution shifts, concept drift, prompt degradation over time

**SupportPilot Hook (1 sentence):** "SupportPilot v1 deployed prompt changes blindly — 40% user complaints, 4h manual rollback. This chapter shows how v4 achieves zero manual interventions in 60 days."

**Cross-refs:** → Ch6 (Prompt Design), Ch9 (Evaluation methodology), Ch10 (Provider routing), Ch14 (Infra SLOs)

**Code Label:** None (conceptual)

---

### 2. Mental Model (350 words)

**Framework:** LLMOps-Lebenszyklus als 5 Phasen mit **Decision Gates** (nicht nur Aktivitäten)

| Phase | Gate (Entry→Exit Criteria) | Tools | Failure Mode if Skipped |
|-------|----------------------------|-------|-------------------------|
| 1. Experiment | Hypothesis → Prompt v0 + Golden Set baseline (Ch9) | Jupyter, Langfuse, promptfoo | Vibe-driven prompts, no baseline |
| 2. Versioning | Prompt vN + eval results + data snapshot tagged | Git + Jinja2 + DVC/LakeFS + Model Card | Unreproducible "works on my machine" |
| 3. CI/CD Pipeline | **4 Gates**: Golden Set ✓, Cost ✓, Canary Metrics ✓, Schema ✓ | GitHub Actions, LLM-judge, promptfoo | Blind deploy → prod incidents |
| 4. Canary Deploy | 5% traffic, SLOs held 10min, auto-rollback armed | Kubernetes/Cloud Run, Prometheus, custom controller | Full rollout of regression |
| 5. Production Loop | SLO monitoring → drift detection → feedback → Golden Set refresh | Langfuse/Helicone, Evidently, PagerDuty | Silent degradation → churn |

**Key Insight:** Jede Phase hat **messbare Exit Criteria**. Kein "fühlt sich gut an".

**SupportPilot Beat:** v2 (Month 3) = Phase 1-2 only. v3 (Month 6) = Phase 3-4 added. v4 (Month 10) = Phase 5 closed loop.

**Cross-refs:** Ch9 (Golden Set creation), Ch14 (Canary infra), Ch10 (Provider fallback)

**Code Label:** [Didactic Example] — Phase gate checklist as markdown table

---

### 3. Architecture (400 words)

**Two-Layer Architecture:**

#### Layer A: Versionierung als Fundament (Compile-Time)
```
prompts/
├── classification/
│   ├── v1.j2          # Jinja2 template
│   ├── v2.j2
│   └── metadata.yaml  # version, author, eval_results_ref, model_pin
data/
├── golden-set/
│   ├── v1.jsonl       # DVC-tracked
│   └── v2.jsonl
models/
├── card.yaml          # Enforceable contract: max_latency_ms, max_cost_eur, min_quality_score
```

**Key Patterns:**
- **Prompts als Code:** Jinja2 + Git tags (`prompt/classification@v2.3`) + eval results stored **with** version (not separate)
- **Semantic Prompt Diff:** LLM-judge compares vN vs vN-1 output on Golden Set → quality delta + behavioral summary
- **Datenversionierung:** `dvc add data/golden-set/v3.jsonl` → `dvc push` → CI schema check (`great_expectations` suite)
- **Model Cards als Contracts:** YAML mit enforceable constraints → CI validiert vor Deploy

#### Layer B: CI/CD Pipeline mit 4 Gates (Deploy-Time)
```
┌─────────────────────────────────────────────────────────────┐
│  PR: prompt change + eval run                               │
├─────────────────────────────────────────────────────────────┤
│  GATE 1: Golden Set Gate (Ch9)                              │
│    - Run full eval suite on Golden Set vCurrent             │
│    - PASS: composite_score ≥ baseline - 2pp                 │
│    - FAIL: block merge, show quality delta per metric       │
├─────────────────────────────────────────────────────────────┤
│  GATE 2: Cost Gate                                          │
│    - Token accounting per test case (input+output)          │
│    - PASS: avg_cost/query ≤ baseline × 1.1                  │
│    - FAIL: block, show cost breakdown by prompt section     │
├─────────────────────────────────────────────────────────────┤
│  GATE 3: Canary Metrics Gate (NEW)                          │
│    - Deploy to canary namespace (5% traffic)                │
│    - Wait 10min, collect: quality SLO, cost SLO, latency SLO│
│    - PASS: all 3 SLOs held → auto-promote to 100%           │
│    - FAIL: auto-rollback, annotate PR with metrics          │
├─────────────────────────────────────────────────────────────┤
│  GATE 4: Schema/Contract Validation                         │
│    - Model Card constraints: latency < 2500ms, cost < €0.02 │
│    - Output schema (JSON Schema / Pydantic) validation      │
└─────────────────────────────────────────────────────────────┘
```

**SupportPilot Beat:** v3 introduced Gates 1-2. v4 added Gates 3-4 + LLM-judge in Gate 1.

**Code Examples Needed (2):**
1. GitHub Actions workflow with 4 gates [Production Ready]
2. Model Card YAML + CI validation script [Production Ready]

**Cross-refs:** Ch6 (Jinja2 patterns), Ch9 (Golden Set, LLM-judge), Ch14 (Canary infra), Ch10 (Provider model pinning)

---

### 4. Core Concepts (500 words)

#### 4.1 SLO/SLI Definitions für LLM-Qualität (NEW — separates from Ch14 infra SLOs)

| SLI | Definition | SLO Target | Measurement |
|-----|------------|------------|-------------|
| Hallucination Rate | % responses with unverifiable claims (LLM-judge + RAGAS) | < 2% | Golden Set eval weekly + production sample (n≥200/day) |
| Factual Accuracy | % claims grounded in retrieved context (RAGAS faithfulness) | > 90% | Same as above |
| Coherence Score | Semantic consistency (embedding cosine self-similarity) | > 0.85 | Production sample, sliding 1h window |
| Relevance | User intent match (LLM-judge on production logs) | > 0.80 | Thumbs up/down + explicit feedback |
| **Composite Quality** | 0.4×factual + 0.3×coherence + 0.3×relevance | > 0.82 | Primary SLO for alerting |

**Cost SLI:** €/query (blended across models, includes caching) | SLO: < €0.015 (SupportPilot tier-1)
**Latency SLI:** E2E P95 (load balancer → first token + stream complete) | SLO: < 2.5s

**Why separate from Ch14:** Ch14 = infra (CPU, memory, network, pod restarts). Ch15 = *model behavior*. Combined dashboard in Grafana: infra row + model quality row.

#### 4.2 Drift Detection Algorithms (Code + Thresholds)

| Drift Type | Algorithm | Threshold | Action |
|------------|-----------|-----------|--------|
| **Input Distribution (Numeric)** | KS-Test on token length, num entities, language prob | p < 0.001 (Bonferroni-corrected) | Alert + tag for Golden Set refresh |
| **Input Distribution (Categorical)** | PSI (Population Stability Index) on intent clusters | PSI > 0.2 | Alert + auto-trigger embedding drift check |
| **Embedding Drift** | Cosine similarity shift: mean(cos(emb_prod, emb_golden)) | < 0.85 (calibrated on 30d history) | Auto-canary previous prompt version |
| **Concept Drift** | Label distribution shift (user feedback labels) | Chi-square p < 0.01 | Retrain/finetune trigger (Ch18) |
| **Quality Drift** | Composite SLO breach (see 4.1) | > 5pp drop vs 7d rolling avg | Incident runbook: Quality Drop |

**Implementation:** Evidently AI custom metrics + Prometheus exporter → Alertmanager → PagerDuty

#### 4.3 Cost Anomaly Detection (Proactive, not reactive)

- **Baseline:** Rolling 7-day median cost/query per prompt version per feature
- **Anomaly:** Current hour cost/query > 2× baseline, p < 0.01 (Mann-Whitney U, n≥50)
- **Attribution:** Which prompt version? Which feature? Which tenant tier?
- **Auto-Mitigation:** Circuit breaker → route to cheaper model (gpt-4o-mini → gpt-3.5-turbo) with quality parity check (composite score delta < 3pp)

#### 4.4 Alert Routing & On-Call (NEW)

| Severity | Condition | Route | Runbook Link | SLA |
|----------|-----------|-------|--------------|-----|
| SEV1 | Composite quality SLO breach > 10pp OR provider outage | PagerDuty (page) + Slack #mlops-alerts | `/runbooks/quality-drop.md` | Acknowledge 5min, mitigate 30min |
| SEV2 | Cost anomaly 2× baseline OR embedding drift PSI > 0.25 | PagerDuty (notify) + Slack | `/runbooks/cost-spike.md` | Acknowledge 15min, mitigate 2h |
| SEV3 | Input drift KS-test p<0.001 OR quality SLO breach 5-10pp | Slack only (no page) | `/runbooks/drift-detected.md` | Triage 1h, resolve 24h |

**Runbook Link in Alert:** Alertmanager annotation `runbook_url` → opens Confluence/GitBook runbook directly.

**Cross-refs:** Ch14 (Alertmanager/PagerDuty config reuse), Ch9 (eval metrics), Ch10 (provider outage detection)

**Code Examples Needed (3):**
1. SLO/SLI definitions as Prometheus rules [Production Ready]
2. Drift detection: KS-test + PSI + embedding drift Python module [Production Ready]
3. Cost anomaly detection + circuit breaker [Production Ready]

---

### 5. Production Example: SupportPilot v1→v4 (400 words)

**This REPLACES the copied Autornotiz. Woven through chapter as narrative thread.**

#### Autornitiz (Chapter Opener) — 150 words
> "Monat 1: SupportPilot deployed prompt updates per `git push production`. Kein Monitoring. Ein Prompt-Change → 40% Nutzer beschweren sich über Halluzinationen. Rollback: 4 Stunden, manuell, nachts.
>
> Monat 3: Langfuse Tracing hinzugefügt. Request/Response, Latenz, Tokens, Thumbs-Up/Down. Kosten-Creep (+15%/Woche) entdeckt. Aber: Quality Drift (Halluzination 8%→18% in 2 Wochen) **nicht** — keine Quality SLOs, kein automatisiertes Eval.
>
> Monat 6: SLOs definiert (Quality Composite > 0.82, Cost < €0.015, P95 < 2.5s). PagerDuty Alerts mit Runbook-Links. Provider stiller Model-Upgrade (gpt-4o-mini Snapshot) → Quality SLO Breach → Alert → Auto-Rollback auf gepinnten Model in 3 Minuten.
>
> Monat 10 (heute): Prompt A/B Framework (statistische Signifikanz, Guardrails). Feedback Loop: Thumbs → Annotation Queue → Golden Set Refresh wöchentlich. Embedding Drift Detection (PSI auf Input-Clustern). Cost Anomaly: 2× Baseline → Circuit Breaker zu günstigerem Model.
>
> **Resultat:** 60 Tage, **null manuelle Interventionen**. MLOps = Eval-Driven Dev Loop + Production SLOs + Automated Drift Response."

#### Narrative Beats Per Section

| Section | SupportPilot Beat |
|---------|-------------------|
| 1. Why this matters | v1 pain: blind deploy → 4h outage |
| 2. Mental Model | v2 = Phase 1-2 only; v3 = Phase 3-4; v4 = Phase 5 |
| 3. Architecture | v3: Gates 1-2 added; v4: Gates 3-4 + LLM-judge |
| 4. Core Concepts | v3: SLOs defined; v4: drift algos, cost anomaly, alert routing |
| 6. Trade-offs | v4: A/B test framework chose prompt v12 over v11 (guardrail: cost) |
| 7. Failure Modes | v3 incident: provider silent upgrade → auto-rollback saved 30min |
| 8. Evaluation | v4: production feedback → Golden Set v5 → eval → canary → promote |
| 9. Best Practices | v4: Model Card contracts prevented bad model deploy |
| 10. Anti-Patterns | v1: "just ship it"; v2: "infra obs = model obs" |

**Code Label:** None (narrative)

---

### 6. Trade-offs (300 words)

#### 6.1 Prompt A/B Testing Framework (Statistical Rigor vs Speed)

| Dimension | Strict (v4 SupportPilot) | Loose (v2) |
|-----------|--------------------------|------------|
| **Minimum Sample Size** | Power analysis: 80% power, α=0.05, MDE=3pp → n=1,200 per variant | "Run until we feel confident" |
| **Guardrail Metrics** | Cost/query ≤ baseline × 1.1, Latency P95 ≤ baseline × 1.2, Hallucination ≤ baseline + 1pp | None |
| **Promotion Criteria** | Primary: Composite quality +3pp, ALL guardrails held | Primary only |
| **Duration** | Min 7 days, max 21 days (seasonality) | 1-2 days |
| **Auto-Promote** | Yes, if all criteria met | Manual |

**SupportPilot Decision:** Chose strict. Cost: 7-21 days per prompt iteration. Benefit: Zero bad promotions in 60 days.

#### 6.2 Cost vs Quality (Explicit Pareto Frontier)

- **SupportPilot Tier-1 (Enterprise):** Quality SLO primary, cost secondary (€0.025/query budget)
- **Tier-2 (SMB):** Cost SLO primary (€0.008/query), quality floor (composite > 0.75)
- **Tier-3 (Free):** Cheapest model, best-effort quality

**Architecture:** Model Router (Ch10) selects model per tier per request. Cost anomaly detection respects tier budgets.

#### 6.3 Drift Detection Sensitivity vs False Positives

| Threshold | False Positive Rate | Detection Delay | SupportPilot Choice |
|-----------|---------------------|-----------------|---------------------|
| PSI > 0.1 | High (weekly) | Fast (hours) | — |
| PSI > 0.2 | Medium (monthly) | Medium (1-2 days) | ✅ Calibrated on 90d history |
| PSI > 0.3 | Low (quarterly) | Slow (weeks) | — |

**Lesson:** Kalibriere auf **deinen** historischen Daten, nicht Papier-Werte.

**Cross-refs:** Ch9 (statistical testing in eval), Ch10 (model router), Ch14 (cost monitoring)

**Code Label:** [Production Ready] — A/B test framework config + power calculation

---

### 7. Failure Modes (400 words)

**Three Concrete Incident Runbooks (replace generic 5-step)**

#### Runbook 1: Quality Drop (SEV1)
**Detection:** Composite quality SLO breach > 10pp vs 7d rolling avg (n≥100 samples in 1h window)
**Alert:** PagerDuty page + Slack #mlops-alerts with `runbook_url`
**Mitigation (Auto, <2 min):**
1. Auto-rollback prompt to last version passing Golden Set Gate
2. Pin model to last known-good snapshot (provider API)
3. Circuit breaker: route 100% traffic to fallback model (quality parity verified)
**Escalation:** If auto-rollback fails → page ML Engineer + PM
**Post-Mortem Template:** Root cause (prompt? model? data?), detection latency, mitigation effectiveness, Golden Set gap analysis

#### Runbook 2: Cost Spike (SEV2)
**Detection:** Cost/query > 2× rolling 7-day median, p<0.01 (Mann-Whitney U, n≥50), attributed to prompt version + feature + tenant tier
**Alert:** PagerDuty notify + Slack (no page)
**Mitigation (Auto, <5 min):**
1. Circuit breaker: route affected feature/tier to cheaper model
2. Quality parity check: composite score delta < 3pp on Golden Set sample (n=50)
3. If parity fails → alert SEV1, manual intervention
**Escalation:** If circuit breaker triggers >3×/day → page FinOps + ML Engineer
**Post-Mortem:** Root cause (prompt bloat? model change? traffic shift?), attribution accuracy, tier impact

#### Runbook 3: Provider Outage (SEV1)
**Detection:** Provider error rate > 5% for 2min OR latency P99 > 30s (Ch10 circuit breaker metrics)
**Alert:** PagerDuty page (shared with Ch10 on-call)
**Mitigation (Auto, <30 sec — Ch10 Semantic Router):**
1. Failover to secondary provider (Anthropic ↔ OpenAI)
2. Quality parity: run 10 Golden Set samples on fallback → composite delta < 3pp
3. Cost delta check: < 2× primary cost
4. Auto-failback when primary healthy 10min (health check endpoint)
**Escalation:** If no healthy provider → page Platform + ML Engineer, activate degraded mode (cached responses)
**Post-Mortem:** Provider communication, failover latency, quality impact, cost impact

**Shared Infrastructure:** All runbooks stored as markdown in `/runbooks/`, versioned with code, linked in Alertmanager annotations.

**SupportPilot Beat:** v3 provider upgrade incident → Runbook 1 executed auto-rollback in 3 min. v4 cost spike → Runbook 2 circuit breaker saved €2,400/day.

**Cross-refs:** Ch10 (Semantic Router, circuit breaker), Ch14 (Alertmanager/PagerDuty config), Ch16 (Security incident runbook — future)

**Code Examples Needed (3):**
1. Runbook 1: Quality Drop — Prometheus alert rule + auto-rollback script [Production Ready]
2. Runbook 2: Cost Spike — anomaly detection + circuit breaker [Production Ready]
3. Runbook 3: Provider Outage — health check + failover logic (references Ch10) [Production Ready]

---

### 8. Evaluation (300 words)

**Two-Loop Evaluation System:**

#### Loop A: CI Gate (Pre-Deploy) — Golden Set Gate
- **Source:** Ch9 Golden Set (curated, versioned, DVC-tracked)
- **Execution:** Every PR runs full eval suite on Golden Set vCurrent
- **Metrics:** Hallucination, Factual Accuracy, Coherence, Relevance, Composite
- **Gate:** Composite ≥ baseline - 2pp AND no metric regression > 3pp
- **LLM-Judge:** Replaces keyword matching — semantic eval on open-ended tasks
- **Output:** PR comment with per-metric delta, pass/fail, link to Langfuse trace

#### Loop B: Production → Golden Set Refresh (Post-Deploy) — Feedback Loop
```
Production Traffic
       │
       ▼
User Feedback (Thumbs Up/Down + Explicit Correction)
       │
       ▼
Annotation Queue (Label Studio / custom UI) — daily triage
       │
       ▼
Verified Samples → Golden Set Candidate Pool
       │
       ▼
Weekly: ML Engineer reviews candidates → Golden Set vN+1
       │
       ▼
DVC commit + tag → CI re-runs on new Golden Set → baseline updates
       │
       ▼
Canary Deploy with new baseline
```

**SupportPilot v4:** Weekly refresh, ~50 new samples/week, 90% precision on candidate selection.

**Drift Detection as Continuous Eval (Section 4.2):**
- KS-test, PSI, Embedding Drift run hourly on production embeddings
- Results fed to Alertmanager → runbooks
- Also: weekly drift report → Golden Set refresh prioritization

**Cross-refs:** Ch9 (Golden Set creation, LLM-judge), Ch14 (production metrics pipeline), Ch18 (concept drift → finetune trigger)

**Code Examples Needed (2):**
1. Golden Set Gate CI step with LLM-judge [Production Ready]
2. Feedback loop: annotation queue → DVC commit automation [Production Ready]

---

### 9. Best Practices (250 words)

| Practice | Implementation | SupportPilot Evidence |
|----------|----------------|----------------------|
| **Model Card als Contract** | YAML mit enforceable constraints → CI validation | Prevented gpt-4o deploy (latency SLO breach) |
| **Prompt Semantic Diff** | LLM-judge compares vN vs vN-1 on Golden Set → quality delta + behavioral summary | Caught "subtle tone change" that keyword diff missed |
| **Alert Runbook Links** | Alertmanager annotation `runbook_url` → direct to markdown runbook | MTTR: 30min → 3min (v3→v4) |
| **Cost Attribution per Feature** | Token accounting middleware + Prometheus labels (feature, prompt_version, tier) | Identified classification prompt v5 as cost driver (+40%) |
| **Data Schema Evolution** | Great Expectations suite on Golden Set → CI gate | Caught schema drift from upstream ticket system |
| **Governance RACI** | Model Owner (ML Eng), Data Steward (Data Eng), PO (Product), Security Owner (Sec Eng) — approval gates in CI | Security Owner gate blocked PII-leaking prompt |
| **Audit Log** | All prompt deploys, model changes, config changes → immutable log (CloudTrail + custom) | SOC2 evidence, incident timeline reconstruction |

**Cross-refs:** Ch6 (prompt structure), Ch9 (eval), Ch10 (provider), Ch14 (audit logging), Ch16 (Security Owner role detail)

**Code Label:** [Production Ready] — Model Card YAML + CI validation, Audit log middleware

---

### 10. Anti-Patterns (200 words)

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| **"Infra Observability = Model Observability"** (SupportPilot v2) | Langfuse traces show latency/tokens, but quality drifts silently | Separate model quality SLOs + automated eval (Ch9) |
| **"Copy-Paste Incident Stories"** (Current Autornotiz) | Same gpt-4o-mini 2024-07-18 anecdote in Ch13 and Ch15 | Write **product-specific** narrative (SupportPilot v1→v4) |
| **"Handwavy Thresholds"** | "Quality < 0.7", "Cost > €0.02" without dataset/n/baseline | Define SLI precisely: metric, dataset, n, measurement method, calibration period |
| **"Golden Set Once"** | Golden Set created in Ch9, never updated | Feedback loop: production → annotation → Golden Set refresh (weekly) |
| **"Manual Rollback Only"** | Incident → human notices → human rolls back → 30-60min | Auto-rollback on SLO breach (canary gate + production monitor) |
| **"Single Provider Dependency"** | Provider outage = total outage | Multi-provider router (Ch10) + quality-parity-checked failover (Ch15) |
| **"Cost as Afterthought"** | Budget alert at 80% = reactive | Proactive: 2× baseline anomaly → circuit breaker → cheaper model |
| **"Prompt Versioning = Git Commits"** | No eval results, no metadata, no semantic diff | Jinja2 + Git tags + eval results stored WITH version + semantic diff |

**SupportPilot Lessons:** v1 had 6/8. v2 had 4/8. v3 had 2/8. v4 has 0/8.

---

### 11. Production Checklist (NEW) (200 words)

**Pre-Deploy (CI Gates)**
- [ ] Golden Set Gate: composite quality ≥ baseline - 2pp on Golden Set vCurrent
- [ ] Cost Gate: avg cost/query ≤ baseline × 1.1
- [ ] Canary Metrics Gate: 5% traffic, 10min, all 3 SLOs held (quality, cost, latency)
- [ ] Schema/Contract Gate: Model Card constraints validated, output schema valid
- [ ] Security Gate (Ch16): PII scan, injection test, tool whitelist validated

**Deploy**
- [ ] Model pinned to specific snapshot (provider/model@date)
- [ ] Canary deployment configured (5%, separate namespace/service)
- [ ] Auto-rollback armed (promote on SLO pass, rollback on SLO fail)
- [ ] Alertmanager rules deployed with `runbook_url` annotations

**Post-Deploy (Day 0-7)**
- [ ] Quality SLOs reporting in Grafana (model quality row + infra row)
- [ ] Drift detection running: KS-test, PSI, embedding drift (hourly)
- [ ] Cost anomaly detection running (hourly, 2× baseline, attributed)
- [ ] Feedback loop active: thumbs → annotation queue → weekly Golden Set review
- [ ] On-call rotation knows runbook locations and escalation paths

**Ongoing (Weekly/Monthly)**
- [ ] Weekly: Golden Set refresh from production feedback
- [ ] Weekly: Drift report review → Golden Set prioritization
- [ ] Monthly: SLO target review (tighten/loosen based on business impact)
- [ ] Monthly: Cost attribution audit → optimization opportunities
- [ ] Quarterly: Incident post-mortem review → runbook updates

**Cross-refs:** Ch14 (infra checklist), Ch16 (security checklist), Ch9 (Golden Set quality)

---

### 12. Exercises (150 words)

**Praxisprojekt: SupportPilot MLOps Pipeline (erweitert)**

**Level 1 — Foundation (2-3h):**
1. Set up Jinja2 prompt structure + Git tags + DVC for Golden Set
2. Implement Golden Set Gate in GitHub Actions (promptfoo + custom LLM-judge)
3. Deploy to canary (5%) with Prometheus metrics export

**Level 2 — Observability (3-4h):**
4. Define 3 SLOs (quality composite, cost, latency) + Prometheus alert rules
5. Implement drift detection: KS-test (token length) + PSI (intent clusters) + embedding drift (cosine)
6. Wire Alertmanager → Slack + PagerDuty with runbook URLs

**Level 3 — Automation (4-5h):**
7. Build cost anomaly detector (2× rolling 7-day median, Mann-Whitney U)
8. Implement circuit breaker: route to cheaper model on cost anomaly + quality parity check
9. Create Feedback Loop: thumbs up/down → Label Studio queue → weekly Golden Set refresh script

**Level 4 — Incident Simulation (2h):**
10. Inject prompt drift (modify prompt → quality drop) → verify auto-rollback < 2min
11. Inject cost anomaly (verbose prompt) → verify circuit breaker triggers
12. Inject provider outage (mock 500 errors) → verify failover < 30s + quality parity

**Success Criteria (messbar):**
- Auto-rollback triggers within 2 min of SLO breach (measured: metric emission → rollback complete)
- Cost anomaly detection: 0 false positives in 7 days baseline, detects injected 2× spike within 1 hour
- Drift detection: PSI > 0.2 on injected distribution shift → alert within 15 min
- Golden Set refresh: ≥20 verified samples/week added, eval baseline updates without manual intervention

---

### 13. Further Reading (100 words)

| Resource | Why Relevant | Chapter Link |
|----------|--------------|--------------|
| **Chip Huyen, "Designing Machine Learning Systems" (Ch7-8)** | Production ML loops, drift detection, monitoring | Mental Model, Core Concepts |
| **Martin Kleppmann, "Designing Data-Intensive Applications" (Ch9)** | SLO/SLI philosophy, drift as data distribution shift | Core Concepts (SLOs) |
| **Alex Xu, "System Design Interview" (Vol 2, Ch12)** | ML system design: monitoring, A/B testing, fallback | Architecture, Trade-offs |
| **Langfuse Docs — "Evaluation in Production"** | Tracing + eval integration, feedback loops | Production Example, Evaluation |
| **Evidently AI — "Data Drift Detection"** | KS-test, PSI, embedding drift implementations | Core Concepts (Drift Algos) |
| **Google SRE Workbook — "Service Level Objectives"** | SLO/SLI/SLA definitions, error budgets | Core Concepts (SLOs) |
| **OpenAI Cookbook — "Prompt Versioning"** | Jinja2 + versioning patterns | Architecture (Versioning) |
| **DVC Docs — "Data Versioning"** | `dvc add/push`, pipelines, CI integration | Architecture (Data Versioning) |
| **Model Card Toolkit (Google)** | Model Card standard + enforceable constraints | Best Practices |
| **PagerDuty — "Runbook Best Practices"** | Runbook structure, alert routing, post-mortems | Failure Modes |

---

## Code Examples Summary (12 Total)

| # | Example | Section | Label |
|---|---------|---------|-------|
| 1 | GitHub Actions 4-Gate Pipeline | 3. Architecture | [Production Ready] |
| 2 | Model Card YAML + CI Validation | 3. Architecture | [Production Ready] |
| 3 | SLO/SLI Prometheus Rules | 4. Core Concepts | [Production Ready] |
| 4 | Drift Detection: KS-test + PSI + Embedding Drift | 4. Core Concepts | [Production Ready] |
| 5 | Cost Anomaly Detection + Circuit Breaker | 4. Core Concepts | [Production Ready] |
| 6 | Runbook 1: Quality Drop Auto-Rollback | 7. Failure Modes | [Production Ready] |
| 7 | Runbook 2: Cost Spike Circuit Breaker | 7. Failure Modes | [Production Ready] |
| 8 | Runbook 3: Provider Outage Failover | 7. Failure Modes | [Production Ready] |
| 9 | Golden Set Gate with LLM-Judge | 8. Evaluation | [Production Ready] |
| 10 | Feedback Loop: Annotation → DVC Commit | 8. Evaluation | [Production Ready] |
| 11 | A/B Test Framework Config + Power Calc | 6. Trade-offs | [Production Ready] |
| 12 | Audit Log Middleware | 9. Best Practices | [Production Ready] |

---

## Cross-Reference Map (8 Refs)

| From Section | To Chapter | Anchor | Text |
|--------------|------------|--------|------|
| 1, 3, 4, 8 | Ch6 (Prompt Engineering) | `chap:prompt_engineering` | "Prompt-Design-Patterns (Jinja2, Few-Shot, CoT): \cref{chap:prompt_engineering}" |
| 1, 3, 4, 8, 11 | Ch9 (Evaluation) | `chap:evaluation` | "Golden Set Aufbau, Qualitätsmetriken, LLM-Judge: \cref{chap:evaluation}" |
| 1, 3, 7, 11 | Ch10 (Deployment/Provider) | `chap:deployment` | "Provider-Routing, Circuit Breaker, Model Pinning: \cref{chap:deployment}" |
| 1, 3, 4, 7, 9, 11 | Ch14 (Operations) | `chap:operations` | "Infra-SLOs, Prometheus/Grafana, Alertmanager/PagerDuty: \cref{chap:operations}" |
| 9, 11 | Ch16 (Security) | `chap:security` | "Security Owner Rolle, Input/Output Guards: \cref{chap:security}" |
| 4, 11 | Ch17 (Inference Opt) | `chap:inference_opt` | "Prompt Caching, Output Limits → Cost Optimization: \cref{chap:inference_opt}" |
| 3, 8 | Ch18 (Model Customization) | `chap:model_customization` | "Concept Drift → Finetuning Trigger: \cref{chap:model_customization}" |
| 4, 7 | Ch19 (Caching/Routing) | `chap:caching_routing` | "Semantic Caching, Router, Guardrails: \cref{chap:caching_routing}" |

**Implementation:** Add to `main.tex` preamble:
```latex
% Cross-refs for Chapter 15
% \cref{chap:prompt_engineering}, \cref{chap:evaluation}, \cref{chap:deployment},
% \cref{chap:operations}, \cref{chap:security}, \cref{chap:inference_opt},
% \cref{chap:model_customization}, \cref{chap:caching_routing}
```

---

## Duplicate Content Resolution (6 Overlaps)

| Overlap | Ch15 Treatment | Cross-Ref Line |
|---------|----------------|----------------|
| Quality metrics (hallucination, factual, coherence) | **Use as SLIs** with SLO targets — Ch9 defines *how to measure*, Ch15 defines *production thresholds + alerting* | "Qualitätsmetriken werden in \cref{chap:evaluation} definiert. Hier nutzen wir sie als SLOs." |
| Latency, error rate, availability | **Reference only** — Ch14 owns infra SLOs. Ch15 adds *model quality* SLOs to same dashboard. | "Infrastruktur-SLOs (Latenz, Fehlerquote, Verfügbarkeit): \cref{chap:operations}. Ergänzt um Modell-Qualitäts-SLOs." |
| Cost tracking | **Budget enforcement + anomaly detection** — Ch10 covers provider pricing/routing. Ch15 covers per-feature accounting, chargeback, proactive anomaly response. | "Provider-Kosten & Routing: \cref{chap:deployment}. Hier: Budget-Enforcement, Anomalie-Detection, Chargeback." |
| Provider outage fallback | **Runbook with quality parity check** — Ch10 implements Semantic Router. Ch15 defines failover *criteria* (quality delta < 3pp, latency < 1.5×, cost < 2×) and runbook. | "Semantic Router Implementierung: \cref{chap:deployment}. Failover-Kriterien & Runbook hier." |
| Golden Set in CI | **Gate with quality delta threshold** — Ch9 creates Golden Set. Ch15 uses it as CI gate + production refresh loop. | "Golden Set Erstellung: \cref{chap:evaluation}. CI-Gate + Production-Refresh-Loop hier." |
| Prompt versioning | **Lifecycle: version → test → deploy → rollback → A/B** — Ch6 covers prompt *design*. Ch15 covers prompt *lifecycle*. | "Prompt-Design-Patterns: \cref{chap:prompt_engineering}. Prompt-Lifecycle (Version, Test, Deploy, Rollback, A/B) hier." |

---

## Evidence Requirements for Numbers (15+ Metrics)

**Template per metric (in chapter as footnote or appendix table):**
```
Metric: <name>
Baseline: <value> (dataset, n, date)
Current: <value> (dataset, n, date)
Delta: <abs> / <rel>
Scope: <model, prompt version, feature, tier>
What Changed: <prompt vN→vN+1, model snapshot, traffic shift>
Limitations: <sample bias, eval constraints, time window>
Source: <eval run ID, dashboard URL, incident report>
```

**Metrics needing evidence in this chapter:**
1. 80% budget alert threshold → reaction window analysis
2. 2× baseline cost anomaly → statistical basis, false positive rate
3. 2 min canary detection → measurement method (metric emission → alert)
4. 99.95% availability → infra vs model availability definition
5. Quality composite > 0.82 SLO → SLI definition, dataset, n, confidence interval
6. Cost/query < €0.015 SLO → model, token breakdown, pricing date
7. Latency P95 < 2.5s SLO → E2E vs API, percentile method, load level
8. PSI > 0.2 threshold → calibration on 90d production data
9. KS-test p<0.001 → Bonferroni correction, false positive rate
10. Embedding drift cosine < 0.85 → calibration on production traffic
11. Hallucination < 2% SLO → measurement method (LLM-judge? human?), n, CI
12. 5% traffic canary → statistical power calculation
13. Guardrail: cost ≤ baseline × 1.1 → justification
14. Guardrail: quality delta < 3pp on fallback → calibration
15. Feedback loop: 50 samples/week → precision/recall of candidate selection

**Note:** SupportPilot numbers are *illustrative* — mark as "Beispielwerte aus SupportPilot v4 (Monat 10), anpassen an dein System" with footnote referencing evidence template.

---

## Writing Notes for Chapter-Writer

1. **Tone:** Senior developer, direct, no hedging. "MLOps ohne SLOs ist Blindflug."
2. **No year references** (AGENTS.md: timeless). Use "aktuell" / "in der Praxis" not "2026".
3. **Every code snippet** labeled `[Production Ready]` or `[Didactic Example]`.
4. **SupportPilot narrative** woven throughout — not isolated in Autornotiz.
5. **Cross-refs** as `\cref{...}` with one-sentence context.
6. **Merke boxes** for key takeaways (mdframed `\merke{...}`).
7. **Warnung boxes** for anti-patterns (`\warnung{...}`).
8. **Praxisbox** for exercises (`\praxishinweis{...}`).
9. **Target ~3,000 words** — cut ruthlessly, prefer code + tables over prose.
10. **German language** — babel `german`, all body text German.

---

## Ready for Chapter-Writer

**Deliverables this outline provides:**
1. ✅ 13-section skeleton with word budgets
2. ✅ Section content detail with tables, algorithms, thresholds
3. ✅ 12 code examples needed with labels
4. ✅ Cross-reference map (8 refs, implementation snippet)
5. ✅ SupportPilot v1→v4 narrative beats per section
6. ✅ Evidence requirements for 15+ numbers
7. ✅ Duplicate content resolution (6 overlaps)
8. ✅ Anti-patterns from research gaps
9. ✅ Production checklist (NEW)
10. ✅ Exercises with measurable success criteria

**Next:** `chapter-writer` agent produces `chapters/15_mlops_observability.tex` from this outline.