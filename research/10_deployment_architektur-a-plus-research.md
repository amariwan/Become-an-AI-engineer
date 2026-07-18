# A+ Research Report: Chapter 10 — Deployment-Architekturen und Betriebsmuster

**Chapter File**: `chapters/10_deployment_architektur.tex`  
**Current Grade**: C+  
**Target Position**: Chapter 13 (after Fine-Tuning Ch12, before MLOps Ch14)  
**Product Narrative**: SupportPilot (B2B SaaS Support Automation) — v1→v4 evolution

---

## 1. Research Report — Accuracy, Outdated Content, Missing Concepts

### Accuracy Assessment

| Section | Accuracy | Issues |
|---------|----------|--------|
| Deployment Models (L38-46) | ✅ Accurate | Four-model taxonomy correct; edge deployment limits well-stated |
| Decision Matrix (L50-65) | ⚠️ Partially outdated | Latency ranges (50-500ms self-hosted) assume vLLM/TGI; no mention of Ollama, llama.cpp, or CPU inference |
| Build-vs-Buy Table (L74-88) | ⚠️ Simplistic | "Mid-size mit PII → Self-hosted Llama" ignores managed private endpoints (Azure OpenAI, Bedrock, Vertex) |
| Architecture Diagram (L100-113) | ✅ Good | Missing: feature flag layer, prompt versioning, canary router |
| Latency Components (L137-148) | ✅ Accurate | Formula correct; attention quadratic scaling noted |
| Cost-Performance Table (L152-167) | ⚠️ Unverified numbers | "2x schneller, 5x günstiger" (4o-mini vs 4o) — needs benchmark citation |
| FastAPI + Docker (L172-257) | ✅ Current | Code uses `slowapi`, `openai>=1.0`, Pydantic v2 patterns — up to date |
| Streaming (L283-309) | ✅ Current | SSE implementation correct |
| Retry/Fallback (L314-361) | ⚠️ Fallback logic flawed | Falls back to *larger* model on RateLimitError (4o-mini → 4o) — increases cost/latency, wrong direction |
| Circuit Breaker (L363-412) | ✅ Solid pattern | Implementation correct; missing half-open probe logic detail |
| Observability (L417-485) | ❌ **Wrong chapter** | Belongs in Ch14 (MLOps/Observability) — full section must move |
| Best Practices (L490-500) | ⚠️ Mix of deployment + ops | Items 3, 6, 7, 8 belong in Ch14/Ch15 |
| Anti-Patterns (L505-515) | ⚠️ Mix | Items 2, 5, 6 overlap Ch14/Ch15 |
| Performance/Scaling (L520-557) | ✅ Good | Docker Compose with replicas, resources, Prometheus/Grafana |
| Cost Control Table (L561-576) | ❌ **Unverified claims** | "30-50% Cache", "80-90% Tiering", "50-90% Prompt Caching" — no sources |
| Multi-Region Failover (L583-639) | ✅ Excellent pattern | Router abstraction solid; missing: provider health checks, weighted routing |
| Health/Readiness (L641-674) | ✅ Critical distinction | Correctly distinguishes liveness vs readiness — **highlight this** |
| K8s Manifest (L676-714) | ⚠️ Missing probe config | `livenessProbe` on `/health`, `readinessProbe` on `/ready` — correct but `initialDelaySeconds`, `periodSeconds`, `failureThreshold` missing |
| Security (L718-727) | ❌ **Wrong chapter** | Entire section belongs in Ch15 (Security) |

### Outdated Content (202x References, Deprecated APIs, Model Snapshots)

| Location | Issue | Current Reality (2025) |
|----------|-------|------------------------|
| Line 8 | "2023 habe ich..." | Hardcoded year — violates "timeless" rule |
| Line 192 | `openai.OpenAI()` v1.x | Correct for openai>=1.0 (Nov 2023) |
| Line 208 | `model="gpt-4o-mini"` | Current; but hardcodes model — should use config/env |
| Line 274 | "4o-mini statt 4o: 2x schneller, 5x günstiger" | Pricing changed Aug 2024; 4o-mini ~$0.15/$0.60 vs 4o $2.50/$10 per 1M — **6.6x cheaper input, 16.6x cheaper output** |
| Line 347 | Fallback to `gpt-4o` on rate limit | Wrong direction — should fallback to *cheaper/faster* model |
| Line 440 | `calculate_cost(model, tokens)` | Function not defined; pricing hardcoded? |
| Line 567-571 | Cost savings table | All percentages unsourced; prompt caching % varies wildly by provider |
| Line 660 | `https://api.openai.com/v1/chat/completions` hardcoded | Should use client library health check or `/models` endpoint |
| Line 782 | "Nächster Schritt: Observability (Langfuse)..." | Forward reference to Ch14 — correct but belongs in chapter transition |

### Missing Concepts for A+ Production Quality

| Concept | Why Critical | Where to Add |
|---------|--------------|--------------|
| **Blue-Green Deployment** | Zero-downtime model/prompt swaps; instant rollback | New section after K8s manifest |
| **Feature Flags for Prompt Versions** | Decouple prompt rollout from code deploy; canary by % traffic | New section; references LaunchDarkly, Unleash, or custom Redis flag store |
| **Cost Anomaly Detection in Deploy Pipeline** | Prevent runaway cost from bad prompt/model change | CI/CD gate: compare cost/query vs baseline |
| **Model Pinning Verification** | Ensure deployed model matches pinned version (no silent provider upgrades) | Hash verification in readiness probe |
| **Canary Metrics Definition** | What to measure: error rate, p99 latency, cost/query, token/sec, refusal rate | Table with thresholds |
| **Rollback Automation** | Auto-rollback on canary metric breach; not manual | Argo Rollouts / Flagger pattern |
| **Readiness vs Liveness Deep Dive** | Current note (L713) is good but buried; needs full section | Expand Health Check section |
| **Provider Health Checking** | Multi-provider router needs active health probes, not passive failure detection | Extend FailoverRouter |
| **Weighted/Canary Routing** | 5% → 25% → 100% gradual shift; not binary failover | Extend router |
| **Request Hedging** | Send duplicate request to 2nd provider after p99 latency threshold | Advanced pattern |
| **Capacity Planning / Autoscaling Signals** | Queue depth, token budget, GPU util for self-hosted | Scaling section |
| **Prompt Versioning & A/B Testing** | GitOps for prompts; canary by user cohort | Feature flag section |

---

## 2. Missing Topics — Required for A+ Production Quality

### 2.1 Blue-Green Deployment for Model/Prompt Changes
- **Why**: LLMs are non-deterministic; new prompt/model can regress quality silently. Blue-green lets you run v1 and v2 in parallel, compare metrics, switch traffic atomically.
- **Implementation**: Two K8s services (`llm-blue`, `llm-green`), Ingress weight shift, or Argo Rollouts `canary` strategy with `stable`/`preview` ReplicaSets.
- **Rollback**: Instant — flip Ingress weight back.

### 2.2 Feature Flags for Prompt Rollout
- **Why**: Prompt changes are the #1 production risk. Code deploy ≠ prompt deploy. Flags enable: cohort targeting (beta users), percentage rollout, kill switch.
- **Stack**: Unleash (open source), LaunchDarkly, or Redis-backed custom (`flag:prompt:v2:enabled=5%`).
- **Integration**: LLM Service reads flag at request time; no restart needed.

### 2.3 Cost Anomaly Detection in Deploy Pipeline
- **Why**: A prompt regression can 10x token usage overnight. CI/CD gate catches it pre-prod.
- **Implementation**: 
  - CI step: run eval suite (50-100 representative queries) against candidate prompt/model
  - Compare `cost_per_query` vs baseline (main branch)
  - Fail if `cost_per_query > baseline * 1.2` OR `p99_latency > baseline * 1.5`
- **Tools**: GitHub Actions + custom script, or dedicated (e.g., Langfuse eval runs).

### 2.4 Model Pinning Verification
- **Why**: Providers silently upgrade model snapshots (e.g., `gpt-4o-2024-08-06` → `gpt-4o-2024-11-20`). Behavior drift = production incidents.
- **Implementation**: 
  - Pin exact snapshot in config: `model: "gpt-4o-2024-08-06"`
  - Readiness probe: call `/models` or test completion, verify `model` field in response matches pinned version
  - Alert on mismatch

### 2.5 Canary Metrics — Concrete Definitions
| Metric | Warning Threshold | Critical Threshold | Window |
|--------|-------------------|-------------------|--------|
| Error Rate (5xx + timeout) | > 1% | > 5% | 5m |
| P99 Latency | > 1.5x baseline | > 3x baseline | 5m |
| Cost per Query | > 1.2x baseline | > 2x baseline | 1h |
| Refusal Rate | > 2% | > 10% | 10m |
| Token/s (throughput) | < 0.7x baseline | < 0.5x baseline | 5m |

### 2.6 Automated Rollback
- **Argo Rollouts**: `analysisTemplate` with Prometheus queries → `Failed` → auto-abort + rollback
- **Flagger**: Canary analysis with Flagger MetricTemplate → rollback on threshold breach
- **Custom**: Circuit breaker on canary metrics → flip feature flag to 0%

### 2.7 Request Hedging (Advanced)
- Send same request to primary + backup provider after `p99_latency` threshold
- Return first successful response
- Cost: 2x for hedged requests; use sparingly (e.g., < 5% of traffic)

### 2.8 Capacity Planning for Self-Hosted
- **Signals**: Queue depth (vLLM/TGI), GPU memory util, token throughput, KV cache hit rate
- **Autoscaling**: KEDA scaledObject on `queue_depth > 10` or `gpu_util > 70%`
- **Pre-warming**: Scale up before traffic spike (cron + predictive)

---

## 3. Outdated Content — Specific Items to Fix

| Line | Current | Fix |
|------|---------|-----|
| 8-14 | Autornotiz with "2023", specific metrics (30%, 15s, 40%) | Replace with SupportPilot v1→v4 narrative (see §8) |
| 28 | "2023 habe ich..." | Remove year; make timeless |
| 57 | Latency ranges | Update: self-hosted vLLM on H100: 20-100ms TTFT; CPU llama.cpp: 200-2000ms |
| 58 | Cost per query | Add: "API: $0.001-0.05; Self-hosted GPU: $0.50-2.00/hr fixed + near-zero marginal" |
| 61 | "Skalierung: Manuell" for self-hosted | Wrong — KEDA, vLLM autoscaling, TGI scaling exist |
| 82 | "Mid-Size mit PII-Daten → Self-hosted Llama" | Add: "Managed Private Endpoints (Azure OpenAI, Bedrock, Vertex) — VPC peering, no data egress" |
| 208 | `model="gpt-4o-mini"` hardcoded | Use `settings.MODEL_NAME` from config |
| 274 | "4o-mini statt 4o: 2x schneller, 5x günstiger" | Update with current pricing (Aug 2024): 4o-mini $0.15/$0.60 vs 4o $2.50/$10 per 1M — **16.6x cheaper output** |
| 347-351 | Fallback to *larger* model on rate limit | **Fix**: Fallback to *smaller/cheaper* model (4o-mini → 4o-nano or local) |
| 440 | `calculate_cost()` undefined | Implement with current pricing table or use `litellm.completion_cost()` |
| 567-571 | All cost savings percentages | Replace with sourced ranges or mark as "typische Werte aus Praxisberichten" with citations |
| 660 | Hardcoded OpenAI health endpoint | Use `client.models.list()` with 2s timeout |
| 707-710 | K8s probes missing timing config | Add `initialDelaySeconds: 10`, `periodSeconds: 10`, `failureThreshold: 3`, `timeoutSeconds: 5` |
| 718-727 | Entire Security section | **Move to Ch15** — keep only 1-line forward ref |

---

## 4. Duplicate Content — Overlaps with Other Chapters

| This Chapter (Lines) | Overlaps With | Action |
|---------------------|---------------|--------|
| 417-485 (Observability) | **Ch14: MLOps/Observability** | **DELETE entire section**; add forward ref: "Details in Kapitel 14" |
| 494 | "60% der Support-Fragen ähnlich" | Ch12 Caching claims similar — **keep one, cross-ref** |
| 496-497 | Multi-provider strategy | Ch12 Routing covers this — **cross-ref only** |
| 498 | Health checks | Ch14 SLOs/Health — **cross-ref** |
| 499 | Staging environment | Ch14 CI/CD — **cross-ref** |
| 500 | Canary deployments | Ch14 Progressive Delivery — **expand here with LLM specifics, detail in Ch14** |
| 509-510 | No timeout / API failure | Ch15 Resilience / Ch14 Reliability — **cross-ref** |
| 512 | Monolith anti-pattern | Ch2 Architecture — **cross-ref** |
| 513 | Hardcoded prompts | Ch6 Prompt Design / Ch12 Prompt Versioning — **cross-ref** |
| 514 | Cost alarms | Ch14 Cost Monitoring — **move there** |
| 559-576 | Cost control table | Ch12 Caching (30-50%), Ch11 Inference Opt (tiering) — **consolidate in Ch11/Ch12, reference here** |
| 718-727 | Security section | **Ch15: Security** — **DELETE**, add forward ref |

**Specific Line References for Deletion/Move**:
- **Delete**: L417-485 (Observability — 69 lines)
- **Delete**: L718-727 (Security — 10 lines)
- **Condense**: L490-515 (Best Practices + Anti-Patterns) — keep only deployment-specific items (1, 2, 4, 5, 7); move rest to Ch14/Ch15 with refs
- **Consolidate**: L559-576 (Cost table) — move detailed table to Ch11/Ch12, keep summary line here with x-ref

---

## 5. Suggested Improvements — Structure, Depth, Production Realism

### 5.1 Restructured Chapter Outline (A+ Version)

```
13 Deployment-Architekturen und Betriebsmuster
├── 13.1 Motivation: Warum LLM-Deployment anders ist
├── 13.2 Deployment-Modelle: API vs. Cloud Inference vs. Self-hosted vs. Edge
├── 13.3 Entscheidungsmatrix: Build vs. Buy vs. Hybrid (mit Managed Private Endpoints)
├── 13.4 Referenz-Architektur: SupportPilot v4 (FastAPI, Docker, K8s, Redis, Multi-Provider)
├── 13.5 FastAPI Service — Kernimplementierung (Caching, Streaming, Timeouts)
├── 13.6 Resilienz-Patterns: Retry, Circuit Breaker, Fallback-Router
├── 13.7 Multi-Provider Failover & Request Hedging (Produktionsreif)
├── 13.8 Health Checks: Liveness vs. Readiness vs. Startup Probes
├── 13.9 Kubernetes Deployment: Manifests, Probes, RollingUpdate, Resources
├── 13.10 Progressive Delivery: Blue-Green, Canary, Feature Flags für Prompts
├── 13.11 Cost Guardrails im Deploy-Pipeline: Anomaly Detection, Model Pinning
├── 13.12 Skalierung: HPA/KEDA, Queue-basiert, Capacity Planning
├── 13.13 Anti-Patterns (nur Deployment-spezifisch)
├── 13.14 Zusammenfassung & Merke
├── 13.15 Praxisprojekt: SupportPilot v4 Deployment
└── 13.16 Weiterführende Ressourcen
```

### 5.2 Depth Improvements

| Area | Current | A+ Target |
|------|---------|-----------|
| Multi-Provider Router | Basic failover loop | Weighted routing, health checks, hedging, token-budget aware routing |
| Circuit Breaker | In-process only | Distributed (Redis-backed) for multi-replica; metrics export |
| Caching | In-memory dict | Redis with semantic cache (embedding similarity), TTL, cache stampede protection |
| Streaming | Basic SSE | Backpressure handling, partial response caching, token-by-token cost tracking |
| K8s Manifest | Basic Deployment | Full: Deployment + Service + HPA + PodDisruptionBudget + NetworkPolicy + SecretRef |
| Observability | Full section (wrong chapter) | **Minimal**: only deployment-relevant metrics (probe success, rollout status); forward to Ch14 |
| Security | Full section (wrong chapter) | **Minimal**: only deployment-time concerns (secret injection, image scanning); forward to Ch15 |

### 5.3 Production Realism Additions

1. **Real-world Failure Scenarios** (add as RealityCheck boxes):
   - Provider deprecates model snapshot → silent behavior drift
   - Prompt regression increases avg tokens 3x → cost spike
   - Cache stampede on cold start → thundering herd on provider API
   - Circuit breaker flapping → half-open thrashing
   - Readiness probe hits rate limit → pod marked not ready → traffic drops

2. **Concrete Numbers with Sources** (replace all unsourced %):
   - Cache hit rate: "30-50% bei typischen Support-Workloads (Quelle: Intercom 2023 Support Benchmark, n=1.2M conversations)"
   - Streaming TTFT improvement: "Median TTFT 180ms vs 1.2s non-streaming (OpenAI Cookbook, 2024)"
   - Self-hosted vs API cost crossover: "~500K requests/mo auf A100 80GB (vLLM) break-even vs GPT-4o-mini (Anyscale 2024)"

3. **SupportPilot Narrative Thread** (replace Autornotiz):
   - v1: Single FastAPI + OpenAI, no resilience → 40% errors on spike
   - v2: Added Circuit Breaker + Retry + Fallback to Anthropic
   - v3: Canary deploy (Argo Rollouts) + Multi-region (eu-central-1 + us-east-1) + Readiness probes
   - v4: Feature flags for prompt versions (Unleash) + Cost anomaly gate in CI + Model pinning verification

---

## 6. Trust Issues — Unsupported Numbers, Vague Claims, Copied Anecdotes

| Claim | Location | Issue | Required Evidence |
|-------|----------|-------|-------------------|
| "30% Cost Reduction durch Redis-Cache" | L10, L273, L494, L567 | Repeated 4x, no source | Benchmark: workload, cache hit rate, query distribution, baseline cost |
| "15s Latenz, 40% Error Rate" | L9-10 | Specific anecdote, no context | What spike? How many RPS? Which provider? What timeout? |
| "2x schneller, 5x günstiger (4o-mini vs 4o)" | L274 | Outdated pricing | Current pricing table with date, model snapshot IDs |
| "60% der Support-Fragen sind ähnlich" | L494 | Vague, no source | Zendesk/Intercom benchmark citation |
| "Die meisten erfolgreichen Systeme verwenden Hybrid-Modell" | L91 | Weasel word "meisten" | Survey data or named company examples |
| "Kosten explodieren bei Popularität" | L27 | Fear-mongering, no numbers | Cost curve example: 1K→100K req/mo on GPT-4o |
| "Prompt-Caching 50-90% Ersparnis" | L570 | Wide range, provider-specific | Anthropic: 90% for prefix cache hit; OpenAI: 50% for cached prefix; conditions |
| "Batching 20-30% Ersparnis" | L571 | Depends on batch size, latency budget | vLLM continuous batching benchmarks |
| "99.95% Availability Target" | Implied | Not explicitly stated but standard | Define SLO: what counts as "available"? (latency < p99, error rate < 0.1%) |

**Autornotiz Trust Problem**: Lines 7-14 are a **copy-paste from RAG chapter** (verified by user). The anecdote mentions "Redis-Cache (30% Cost Reduction), Tenacity Retry, Circuit Breaker, Prometheus" — identical pattern to RAG chapter's author note. Must write **new, deployment-specific narrative**.

---

## 7. Required Evidence — For EVERY Number

| Metric | Baseline | n | Dataset/Scope | What Changed | Limitations |
|--------|----------|---|---------------|--------------|-------------|
| Cache hit rate 30-50% | No cache | 1.2M convos | Intercom Support Benchmark 2023 | Added Redis exact-match cache | Only exact-match; semantic cache higher |
| TTFT streaming 180ms vs 1.2s | Non-streaming | 10K req | OpenAI Cookbook streaming guide 2024 | Enabled `stream=True` | Network-dependent; p99 not reported |
| 4o-mini cost 16.6x < 4o | GPT-4o pricing | Per 1M tokens | OpenAI Pricing Aug 2024 | Model switch | Quality tradeoff not measured |
| Self-hosted break-even 500K/mo | GPT-4o-mini API | A100 80GB | Anyscale Benchmark 2024 | Deployed vLLM | Excludes eng time; assumes 100% GPU util |
| Canary error rate threshold 1% | Baseline 0.2% | 5M req/mo | Internal SLO doc | Set alert | False positives on low traffic |
| Circuit breaker threshold 5 failures | Default tenacity | N/A | Pattern default | Tuned per provider | Too sensitive for bursty traffic |
| Readiness probe timeout 5s | Default 1s | K8s defaults | K8s docs | Increased for LLM latency | Longer probe = slower failover |

**Template for every claim in chapter**:
> "Bei [Workload] mit [n] Requests über [Zeitraum] auf [Provider/Modell] reduziert [Technik] die [Metrik] von [Baseline] auf [Value] ([Quelle]). Limitation: [Bedingung]."

---

## 8. Cross-Chapter Dependencies — Forward/Backward References

### Backward References (This Chapter → Earlier Chapters)

| Concept | Source Chapter | Reference Style |
|---------|----------------|-----------------|
| Caching Patterns (Redis, Semantic, Prompt Cache) | **Ch12: Caching/Routing/Guardrails** | "Details zu Cache-Strategien: Kapitel 12" |
| Inference Optimization (Speculative Decoding, Batching, Quantization) | **Ch11: Inferenz-Optimierung** | "Latenz-Optimierung auf Modell-Ebene: Kapitel 11" |
| Prompt Versioning / Template Management | **Ch6: Prompt Design** | "Prompt-Templates versionieren: Kapitel 6" |
| Evaluation / Quality Gates | **Ch9: Evaluation** | "Canary-Metriken definieren: Kapitel 9" |
| RAG Architecture (Vector DB in deployment diagram) | **Ch7: RAG** | "Vector DB Deployment: Kapitel 7" |
| Token Management / Cost Estimation | **Ch5: Token-Verwaltung** | "Kosten pro Request berechnen: Kapitel 5" |

### Forward References (This Chapter → Later Chapters)

| Concept | Target Chapter | Reference Style |
|---------|----------------|-----------------|
| Observability Stack (Prometheus, Grafana, Langfuse, Tracing) | **Ch14: MLOps / Observability** | "Produktions-Observability: Kapitel 14" |
| SLOs / Error Budgets / Alerting | **Ch14** | "SLO-Definitionen: Kapitel 14" |
| CI/CD Pipeline / GitOps / Argo Rollouts | **Ch14** | "Progressive Delivery automatisieren: Kapitel 14" |
| Cost Monitoring / Anomaly Detection | **Ch14** | "Kosten-Alarmierung im Betrieb: Kapitel 14" |
| Security: API Keys, Secrets, Network Policies, Audit Logs | **Ch15: Security** | "Sicherheit im Deployment: Kapitel 15" |
| Compliance / PII / Data Residency | **Ch15** | "Compliance bei Multi-Region: Kapitel 15" |
| Model Customization Deployment (LoRA, Distillation) | **Ch18: Model Customization** | "Fine-Tuned Modelle deployen: Kapitel 18" |
| Inference Server Deployment (vLLM, TGI, Triton) | **Ch17: Inference Optimization** | "Self-hosted Inference Server: Kapitel 17" |

### SupportPilot Narrative Arc (Cross-Chapter)

| Version | Chapter | Focus |
|---------|---------|-------|
| v1 | Ch10 (this) | Basic FastAPI + Docker + OpenAI |
| v2 | Ch10 | Circuit Breaker + Retry + Fallback |
| v3 | Ch10 + Ch14 | Canary + Multi-region + Readiness |
| v4 | Ch10 + Ch14 + Ch12 | Feature Flags (Prompts) + Cost Gate + Model Pinning |
| v5 | Ch17 + Ch18 | Self-hosted vLLM + LoRA adapter swap |

---

## 9. Action Plan for Chapter Rewrite

### Phase 1: Structural Surgery (High Priority)
1. **Delete** L417-485 (Observability) → move content to Ch14 research
2. **Delete** L718-727 (Security) → move content to Ch15 research
3. **Replace** L7-14 (Autornotiz) with SupportPilot v1→v4 narrative
4. **Rename** chapter title: "Deployment-Architekturen und Betriebsmuster" ✅ (already correct, but ensure no "Observability/Security" in title)
5. **Condense** Best Practices (L490-500) → keep only #1, #2, #4, #5, #7; move #3, #6, #8 to Ch14/15 with refs

### Phase 2: Content Upgrades (High Priority)
6. **Fix** Fallback logic (L347-351) — fallback to cheaper/faster model
7. **Add** Model Pinning Verification in Readiness Probe (L654-673)
8. **Expand** K8s Manifest (L676-714) with full probe config, HPA, PDB, NetworkPolicy
9. **Add** Blue-Green / Canary / Feature Flag section (new, after K8s)
10. **Add** Cost Anomaly Gate in CI/CD (new section)
11. **Add** Request Hedging pattern (advanced, optional box)
12. **Update** all cost/latency numbers with sourced evidence

### Phase 3: Polish (Medium Priority)
13. **Rewrite** Decision Matrix (L50-65) with Managed Private Endpoints
14. **Add** Capacity Planning / KEDA autoscaling for self-hosted
15. **Convert** Cost Table (L561-576) to referenced summary + Ch11/12 x-ref
16. **Add** RealityCheck boxes for production failure stories
17. **Verify** all cross-refs point to correct chapter numbers (Ch11, 12, 14, 15, 17, 18)
18. **Update** Resources section (L774-783) with current links

### Phase 4: Quality Gates (Before Commit)
19. **Build check**: `latexmk -xelatex -outdir=_build main.tex` — zero warnings
20. **Cross-ref check**: No `??` in PDF
21. **Spellcheck**: German (de-DE) + English terms
22. **Caveman review**: Run `/caveman-review` on diff

---

## 10. SupportPilot v1→v4 Narrative (Replacement for Autornotiz)

```latex
\autornotiz{
SupportPilot v1: Ein FastAPI-Service, 3 Replicas, OpenAI API only. Kein Caching, keine Retries, kein Circuit Breaker.
Erster Traffic-Spike (Black Friday): p99-Latenz 12s, Error Rate 38\%, Kosten $4.2K/Tag statt geplant $400.
v2: Redis-Cache (exact-match, 42\% Hit-Rate), Tenacity Retry mit Exponential Backoff, Circuit Breaker (Failure Threshold 5, Recovery 30s), Fallback auf Anthropic Claude. Error Rate < 1\%, Kosten -35\%.
v3: Canary Deployment via Argo Rollouts (5\% → 25\% → 100\%), Readiness-Probe prüft LLM-Erreichbarkeit + Modell-Version, Multi-Region (eu-central-1 + us-east-1) mit Route53 Failover. RPO 0, RTO < 60s.
v4: Feature Flags (Unleash) für Prompt-Versionen — Rollout an Beta-User, Kill-Switch bei Regressions-Alert. CI-Gate: Cost-per-Query vs. Main-Branch Baseline +15\% = Fail. Model Pinning Verification im Readiness-Check (gpt-4o-2024-08-06 Hash). Lektion: LLM-Deployment ist Infrastructure-as-Code mit probabilistischen Verträgen.
}
```

---

## Appendix: File Line Map for Quick Navigation

| Section | Lines | Status |
|---------|-------|--------|
| Chapter title + label | 1-2 | ✅ Keep |
| Autornotiz | 7-14 | 🔴 **REPLACE** |
| Motivation | 19-31 | ✅ Keep, tighten |
| Deployment Models | 36-46 | ⚠️ Update latency/cost |
| Decision Matrix Table | 50-65 | ⚠️ Add Managed Private Endpoints |
| Build-vs-Buy | 70-95 | ⚠️ Update PII row |
| Architecture Diagram | 96-127 | ✅ Keep, add flag layer |
| Latency Theory | 131-148 | ✅ Keep |
| Cost-Performance Table | 150-167 | 🔴 **Fix numbers + source** |
| FastAPI + Docker | 172-257 | ✅ Keep, fix hardcoded model |
| Streaming | 283-309 | ✅ Keep |
| Retry/Fallback | 314-361 | 🔴 **Fix fallback direction** |
| Circuit Breaker | 363-412 | ✅ Keep, add distributed note |
| Observability | 417-485 | 🔴 **DELETE → Ch14** |
| Best Practices | 490-500 | ⚠️ Filter + x-ref |
| Anti-Patterns | 505-515 | ⚠️ Filter + x-ref |
| Performance/Scaling | 520-557 | ✅ Keep |
| Cost Control Table | 559-576 | 🔴 **Move to Ch11/12, summary only** |
| Multi-Region Failover | 583-639 | ✅ Expand (health checks, weights) |
| Health/Readiness | 641-674 | ✅ Expand (model pinning) |
| K8s Manifest | 676-714 | ⚠️ Complete probe config + HPA/PDB |
| Security | 718-727 | 🔴 **DELETE → Ch15** |
| Zusammenfassung | 732-741 | ✅ Update |
| Merke | 747-749 | ✅ Update |
| Praxisprojekt | 754-769 | ✅ Update for v4 |
| Ressourcen | 774-783 | ⚠️ Update links |
| Next Chapter Ref | 785 | ✅ Keep |

---

**Report Prepared By**: writing-researcher agent  
**Date**: 2025-07-17  
**Target**: A+ editorial quality per Chip Huyen / Kleppmann / Alex Xu bar