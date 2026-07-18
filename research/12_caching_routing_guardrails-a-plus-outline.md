# A+ Chapter Outline — Chapter 12: Caching, Routing, Guardrails

**Datei:** `chapters/12_caching_routing_guardrails.tex`
**Position:** Kapitel 10 (Teil 4: Production Layer) — nach Multimodal (Kap. 9), vor Inference Optimization (Kap. 11)
**Produkt-Narrativ:** SupportPilot (B2B SaaS Support-Automatisierung, 10k Req/Tag)

---

## 1. Warum das wichtig ist (Why this matters)

**Kernthese:** Ohne Caching, Routing, Guardrails ist jedes LLM-System in Produktion ein Kosten- und Sicherheitsrisiko. Nicht das Modell entscheidet über Wirtschaftlichkeit — die Infrastruktur drumherum.

**SupportPilot-Eröffnungsstory (ersetzt kopierte E-Commerce-Autornotiz):**
> 2024 habe ich SupportPilot gebaut — B2B Support-Automatisierung, 10.000 Requests/Tag.
> Woche 1: Naives System. Jede Anfrage → GPT-4o. Kosten: $180/Tag. Latenz p99: 4,2 s.
> Woche 3: Three-Tier Cache. Prompt-Cache (KV) für System-Prompt → -60 % Prefill.
> Response-Cache für Statusabfragen ("Wo ist Paket #12345?") → 31 % Exact Hits.
> Semantic-Cache für FAQ ("Wie retouriere ich?" vs "Rückgabe-Prozess") → 28 % Hits @ 94 % Precision (Threshold 0.92).
> Semantic Router: Intent-Klassifikation (Order/FAQ/Complaint/Other) → gpt-4o-mini / Cache / Claude Sonnet / GPT-4o.
> Budget-Guard: Tageslimit $120, User-Quota 20 req/min → verhinderte $2.000 Runaway-Loop bei defektem Webhook.
> Security-Guards (Kap. 16): PII-Masking VOR Cache-Write, Injection-Block, Output-Re-Check.
> Ergebnis: $38/Tag (79 % Ersparnis), p99 1,1 s, 0 PII-Leaks, 0 Budget-Überschreitungen.
> Der Unterschied war nicht das Modell. Es war Disziplin bei Cache, Router, Guardrails — und Messbarkeit.

**Lernziele:**
- Three-Tier Cache (KV / Response / Semantic) architektieren und betreiben
- Semantic Router als First-Class Component: Intent → Model → Cost
- Guardrails als latency-budgeted Pipeline (Input/Output, PII, Injection)
- Budget Controller als Runtime-Circuit-Breaker (Daily Cap, Per-User Quota, Anomaly Detection)
- Evaluation & Observability für Cache-Hitrate, Router-Verteilung, Cost/Request, Budget-Burnrate

**Vorwärtsverweise:** Kap. 11 (Inference Optimization — lokale Embeddings für Cache), Kap. 13 (Model Customization — Router als Fine-Tuning-Kandidat), Kap. 15 (Observability — Cache/Router/Budget Dashboards), Kap. 16 (Security — InputGuard/OutputGuard Deep Dive)

---

## 2. Mentales Modell (Mental Model)

**Analogie:** Drei Verteidigungsebenen einer Burg
- **Außenmauer (KV/Response Cache):** Billig, schnell, exakt — hält 30–40 % der Angriffe (Requests) ab
- **Graben mit Fallen (Semantic Cache):** Fängt ähnliche Angriffe — braucht Kalibrierung (Threshold), sonst Fehlalarme
- **Wachposten mit Orders (Semantic Router):** Entscheidet: Billiger Bogenschütze (Mini) vs. Elite-Krieger (Opus) vs. Diplomat (Sonnet)
- **Schatzkammer-Wächter (Budget Controller):** Zählt Goldmünzen pro Tag, schlägt Alarm bei Anomalie, schließt Tor bei Überschreitung
- **Spione an den Toren (Guardrails):** PII-Maske VOR Eintritt, Injection-Check, Ausgangskontrolle

**Kernentscheidungen (Trade-off Triangle):**
```
           Latency
             ▲
             │
   Accuracy  │  Cost
    (Quality)┼──────►
```
- Cache erhöht Accuracy (konsistente Antworten) UND senkt Cost & Latency — aber Staleness-Risiko
- Router optimiert Cost vs. Quality pro Intent — aber fügt Klassifikations-Latenz hinzu
- Guardrails schützen Safety/Compliance — aber kosten Latency-Budget (Budgetierung Pflicht!)

---

## 3. Architektur (Architecture)

**High-Level Request Flow (SupportPilot):**

```
Request
  │
  ├─► [Input Guard] ──► PII Masking ──► Injection Detect ──► (fail-closed)
  │        │
  │        ▼
  │   [Cache Key Gen] ← masked query + model_version + tenant_id
  │        │
  │        ├─► [KV Cache] ──────► Hit? ──► Return (0ms)
  │        │
  │        ├─► [Response Cache] ─► Hit? ──► Return (5ms)
  │        │
  │        └─► [Semantic Cache] ─► Hit? ──► Return (15ms)
  │                 │
  │                 ▼ (Miss)
  │           [Semantic Router]
  │                 │
  │                 ├─► Intent: ORDER ────► gpt-4o-mini (cheap, fast)
  │                 ├─► Intent: FAQ ──────► Return cached / gpt-4o-mini
  │                 ├─► Intent: COMPLAINT ─► claude-sonnet-4 (empathy)
  │                 └─► Intent: OTHER ────► gpt-4o (fallback)
  │                 │
  │                 ▼
  │           [Budget Controller] ──► Check daily/user quota
  │                 │
  │                 ├─► OK ──► LLM Call
  │                 └─► EXCEEDED ──► Circuit Breaker / Fallback / Alert
  │
  ▼
[Output Guard] ──► PII Re-check ──► Safety Classify (async, fail-open)
  │
  ▼
[Cache Write] ──► Store masked response (key = masked query + model_ver)
  │
  ▼
Response
```

**Komponenten-Übersicht:**

| Komponente | Responsibility | Latency Budget | State |
|------------|----------------|----------------|-------|
| InputGuard | PII-Masking, Injection-Detect | ≤50 ms (sync) | Stateless |
| KVCache | System-Prompt Prefill | 0 ms (provider) | Provider-managed |
| ResponseCache | Exact-match Q&A | ≤5 ms (Redis) | TTL + Versioned Keys |
| SemanticCache | Fuzzy-match FAQ | ≤15 ms (Vector DB) | HNSW Index + Eval |
| SemanticRouter | Intent → Model + Cost | ≤150 ms (cached) | Calibrated Classifier |
| BudgetController | Daily/User limits, Circuit-break | ≤5 ms (Redis) | Redis Counters |
| OutputGuard | PII re-check, Safety | ≤50 ms (async) | Stateless |

**Cross-Chapter Refs:**
- KV-Cache Provider-Spezifika → Kap. 4 (OpenAI/Anthropic Prompt Caching)
- Token-Counting für Keys → Kap. 5
- Embedding-Modellwahl → Kap. 7, Abschnitt 3
- Structured Outputs für Router → Kap. 4 (JSON Mode)
- Golden-Set Methodik → Kap. 9 (Evaluation)
- Provider-Abstraktion → Kap. 3, Listing 3.x
- InputGuard/OutputGuard Implementation → Kap. 16
- Cost Dashboard/Alerting → Kap. 15

---

## 4. Kernkonzepte (Core Concepts)

### 4.1 Three-Tier Cache Stack

| Tier | Was | Key | TTL | Invalidation | Skalierung |
|------|-----|-----|-----|--------------|------------|
| **1. KV-Cache (Prompt Cache)** | Provider-seitiges Prefill-Caching für System-Prompts, Few-Shot | `prompt_hash + model_version` | Provider-managed (5–30 min) | Model-Upgrade → neuer Prompt-Hash | Anthropic `cache_control`, OpenAI auto ≥1024 tok |
| **2. Response Cache** | Exakte Duplikate: Statusabfragen, Config-Lookups | `SHA256(masked_query + model_ver + tenant)` | 1h–24h (config) | Explicit key eviction, Model-Version-Tag | Redis/Valkey Cluster, LRU |
| **3. Semantic Cache** | Ähnliche FAQ-Intents | `embedding(query) → ANN search` | 7–30 Tage | Versioned Index, Re-embed on model change | pgvector/Qdrant/Pinecone HNSW |

### 4.2 Cache Key Design (Production Pattern)

```python
# [Production Ready]
def build_cache_key(
    query: str,
    model_version: str,
    tenant_id: str,
    intent: Optional[str] = None
) -> str:
    """
    Versioned, tenant-isolated, PII-safe cache key.
    Model-Version im Key → Auto-Invalidation bei Model-Upgrade.
    Intent optional für Router-Bypass-Caching.
    """
    masked = redact_pii(query)  # PII-Masking VOR Key-Generierung!
    parts = [tenant_id, model_version]
    if intent:
        parts.append(intent)
    parts.append(hashlib.sha256(masked.encode()).hexdigest()[:16])
    return ":".join(parts)
```

### 4.3 Semantic Router — Deep Home (Ch 3/5 nur Forward-Ref)

**Architektur:**
```
Query → Embedding (gpt-4o-mini classifier OR embedding k-NN)
         │
         ├─► Cached Classification? → Return intent (5ms)
         │
         └─► LLM Classifier (structured output) → Intent + Confidence
                    │
                    ├─► Confidence ≥ threshold → Route to model
                    ├─► Confidence < threshold → Conformal Prediction Set
                    │       ├─► Singleton → Route
                    │       └─► Multi/Empty → Fallback Chain
                    │
                    └─► Fallback Chain:
                            1. Embedding-based k-NN Router (fast, cheap)
                            2. Default Model (gpt-4o)
                            3. Human Escalation Queue
```

**Intent-Schema (SupportPilot):**
```json
{
  "intents": [
    {"name": "ORDER_STATUS", "model": "gpt-4o-mini", "max_cost_usd": 0.002},
    {"name": "FAQ", "model": "semantic_cache", "max_cost_usd": 0.0},
    {"name": "COMPLAINT", "model": "claude-sonnet-4", "max_cost_usd": 0.04},
    {"name": "TECHNICAL", "model": "claude-sonnet-4", "max_cost_usd": 0.04},
    {"name": "BILLING", "model": "gpt-4o", "max_cost_usd": 0.01},
    {"name": "OTHER", "model": "gpt-4o", "max_cost_usd": 0.01}
  ],
  "fallback": "gpt-4o",
  "calibration": {"method": "conformal", "alpha": 0.1}
}
```

### 4.4 Budget Controller — Runtime Cost Governance

```python
# [Production Ready]
class BudgetController:
    def __init__(
        self,
        daily_limit_usd: float,
        per_user_rpm: int,
        per_user_tpm: int,
        redis: Redis,
        alert_webhook: str
    ):
        self.daily_limit = daily_limit_usd
        self.user_rpm = per_user_rpm
        self.user_tpm = per_user_tpm
        self.redis = redis
        self.alert_webhook = alert_webhook

    async def check_and_reserve(
        self,
        tenant_id: str,
        user_id: str,
        estimated_cost_usd: float,
        estimated_tokens: int
    ) -> BudgetDecision:
        """
        Returns: ALLOW | DENY_DAILY | DENY_USER_QUOTA | CIRCUIT_BREAK
        """
        pipe = self.redis.pipeline()
        # Daily spend
        daily_key = f"budget:{tenant_id}:{date.today()}"
        pipe.incrbyfloat(daily_key, estimated_cost_usd)
        pipe.expire(daily_key, 86400 * 2)
        # User RPM
        rpm_key = f"quota:{tenant_id}:{user_id}:rpm"
        pipe.incr(rpm_key)
        pipe.expire(rpm_key, 60)
        # User TPM
        tpm_key = f"quota:{tenant_id}:{user_id}:tpm"
        pipe.incrby(tpm_key, estimated_tokens)
        pipe.expire(tpm_key, 60)
        results = await pipe.execute()

        daily_spend = results[0]
        user_rpm = results[2]
        user_tpm = results[4]

        if daily_spend > self.daily_limit:
            await self._alert("DAILY_LIMIT", tenant_id, daily_spend)
            return BudgetDecision.CIRCUIT_BREAK
        if user_rpm > self.user_rpm or user_tpm > self.user_tpm:
            return BudgetDecision.DENY_USER_QUOTA
        return BudgetDecision.ALLOW
```

### 4.5 Guardrail Integration — Latency-Budgeted

| Guard | Sync/Async | Latency Budget | Fail Policy | Ch 16 Ref |
|-------|------------|----------------|-------------|-----------|
| PII Masking (Input) | Sync | ≤30 ms | Fail-Closed | InputGuard.mask() |
| Injection Detect (Input) | Sync | ≤20 ms | Fail-Closed | InputGuard.detect_injection() |
| PII Re-check (Output) | Async | ≤50 ms | Fail-Open (log only) | OutputGuard.recheck_pii() |
| Safety Classify (Output) | Async | ≤50 ms | Fail-Open | OutputGuard.classify_safety() |

**Gesamt-Budget:** ≤100 ms added latency (50 ms sync input, 50 ms async output)

---

## 5. Produktions-Beispiel: SupportPilot (Production Example)

**Durchgängiges Narrativ — zieht sich durch alle Sections:**

### 5.1 Woche 1: Naiver Baseline
- Jede Anfrage → GPT-4o
- $180/Tag, p99 4,2 s
- Keine Observability

### 5.2 Woche 2: KV-Cache (Prompt Caching)
- System-Prompt 2.1k Tokens → `cache_control: {"type": "ephemeral"}`
- 60 % Prefill-Reduktion, -40 % Input-Cost
- Anthropic: 90 % Prefill gespart bei ≥2k Prefix (Docs 2026-06)
- OpenAI: 50 % Input-Cost Reduction für cached Tokens (Pricing 2026-06)

### 5.3 Woche 3: Response Cache (Exact Match)
- Order-Status: "Wo ist Paket #12345?" → SHA256 Key
- 31 % Exact-Hit-Rate (n=2,3M req/mo)
- Redis Cluster, TTL 1h, Versioned Keys

### 5.4 Woche 3: Semantic Cache (FAQ Cluster)
- Embedding: `text-embedding-3-small` (1536-dim)
- Vector DB: pgvector HNSW (m=16, ef_construction=200)
- Golden Set: 500 FAQ-Queries, 30 Tage Production Logs
- Threshold 0.92 → 28 % Recall, 94 % Precision (SupportPilot, n=500)
- **Calibration:** Threshold NICHT hardcoded — `calibrate(golden_set)` Methode

### 5.5 Woche 4: Semantic Router
- Intent Classifier: `gpt-4o-mini` (Structured Output, ~$0,0001/Call, 150ms p95)
- Cached Classification für wiederholte Intents
- Conformal Prediction: Abstain bei Confidence < 0.85 → Fallback Chain
- Routing: ORDER→mini, FAQ→Cache, COMPLAINT→Sonnet, OTHER→4o
- Cost Savings: 40 % vs. All-Opus Baseline (A/B, n=100k)

### 5.6 Woche 4: Budget Controller
- Daily Cap: $120 (80 % von $150 Plan)
- Per-User: 20 RPM, 50k TPM
- Circuit Breaker bei Anomalie (Z-Score > 3 auf Cost/Req)
- **Runaway Prevention:** Defekter Webhook → 50k req in 10 min → $2.000 verhindert

### 5.7 Woche 5: Security Guards (Ch 16 Forward-Ref)
- Input: PII-Masking (Email, IBAN, Kreditkarte) VOR Cache-Key
- Input: Prompt Injection Detection (Heuristik + Classifier)
- Output: PII Re-Check, Safety Classification (Async, Fail-Open)
- 0 PII-Leaks in 6 Monaten Produktion

### 5.8 End-to-End Metriken (Nach 6 Wochen)
| Metrik | Baseline | Nach Cache/Router/Guards | Delta |
|--------|----------|--------------------------|-------|
| Cost/Tag | $180 | $38 | -79 % |
| p99 Latency | 4,2 s | 1,1 s | -74 % |
| Cache Hit Rate (Total) | 0 % | 59 % | +59 pp |
| — KV Cache | — | 60 % Prefill Reduction | — |
| — Response Cache | — | 31 % Exact Hit | — |
| — Semantic Cache | — | 28 % Hit @ 94 % Prec | — |
| Router Cost Savings | — | 40 % vs All-Opus | — |
| Budget Violations | 3/Monat | 0 | -100 % |
| PII Incidents | 2/Monat | 0 | -100 % |

---

## 6. Trade-offs (Trade-offs)

| Entscheidung | Pro | Contra | Empfehlung |
|--------------|-----|--------|------------|
| **Semantic Cache Threshold** | Höher → mehr Hits, mehr Cost-Saving | Höher → mehr False Positives (falsche Antworten) | Start 0.92 (Support), 0.97 (Medical). Kalibrieren pro Domain. |
| **Router: LLM Classifier vs. Embedding k-NN** | LLM: höhere Accuracy, versteht Nuancen | LLM: +150ms, +$0,0001/Call | Hybrid: LLM für neue/unklar, Embedding-Cache für bekannte |
| **Cache TTL: Kurz vs. Lang** | Kurz: frischere Antworten | Lang: höhere Hit-Rate | FAQ: 7–30 Tage. Order-Status: 1h. Model-Version im Key! |
| **Guardrail Sync vs. Async** | Sync: garantiert blockiert | Sync: addiert Latenz | Input: Sync (Fail-Closed). Output: Async (Fail-Open). |
| **Budget: Hard Limit vs. Soft Alert** | Hard: verhindert Überraschungen | Hard: kann legitime Traffic blockieren | Daily Hard Cap + Per-User Soft Quota + Alerting |
| **PII Masking: Vor vs. Nach Cache** | Vor: keine Leaks, Cache teilt masked | Vor: Key ändert sich bei gleicher Query | **IMMER VOR Cache-Write** — Key = masked Query |

---

## 7. Failure Modes (Failure Modes)

| # | Failure Mode | Symptom | Detection | Mitigation |
|---|--------------|---------|-----------|------------|
| 1 | **Semantic Cache False Positive** | Falsche FAQ-Antwort serviert | Precision-Drop im Eval (Canary), User Complaints | Threshold ↑, Human-in-the-loop für niedrige Confidence, A/B Test |
| 2 | **Cache Stampede** | Cache Miss → 1000 parallele LLM-Calls | Latency Spike, Cost Spike | `asyncio.Lock` per Key / Redis `SET NX` + `GETSET` |
| 3 | **Model Upgrade → Stale Cache** | Alte Antworten mit neuem Model-Verhalten | Version Mismatch in Logs | Model-Version im Cache-Key, `invalidate_by_model_version()` Job |
| 4 | **Router Misclassification** | Complaint → Mini → Schlechte Empathie | Intent Confusion Matrix Drift | Conformal Prediction (Abstain), Fallback Chain, Retraining Trigger |
| 5 | **Budget Controller False Positive** | Legitimer Traffic geblockt (Flash Sale, Outage) | Support Tickets, Revenue Drop | Alert-first (nicht Block) für Daily Cap, User Quota großzügig |
| 6 | **PII Leak via Cache** | User B sieht User A's Email in Antwort | Audit Log, Penetration Test | **PII Masking VOR Cache-Key**, Output Guard Re-Check |
| 7 | **Guardrail Timeout** | Request hängt bei Input Guard | p99 Latency Spike | Hard Timeout (50ms), Fail-Closed für Input, Fail-Open für Output |
| 8 | **Vector DB Ausfall** | Semantic Cache komplett down | Health Check Alert | Graceful Degradation → Response Cache Only → LLM Direct |
| 9 | **Cost Attribution Loss** | Keine Cost/Tenant Visibility | FinOps Beschwerde | Tags auf JEDER Request: `tenant_id, feature, model, intent` |
| 10 | **Runaway Loop ungefangen** | $2000 in 10min | Budget Controller Alert | Circuit Breaker bei Z-Score > 3, Max Steps pro Conversation |

---

## 8. Evaluation (Evaluation)

### 8.1 Semantic Cache Eval Harness (CI Gate)

```python
# [Production Ready] — runs in CI/CD
class SemanticCacheEvaluator:
    def __init__(self, cache: SemanticCache, golden_set: List[GoldenQuery]):
        self.cache = cache
        self.golden = golden_set  # (query, expected_answer, intent)

    def evaluate(self, threshold: float) -> CacheEvalResult:
        hits = 0
        correct = 0
        false_positives = []
        for g in self.golden:
            result = self.cache.lookup(g.query, threshold=threshold)
            if result:
                hits += 1
                if self._equiv(result.answer, g.expected):
                    correct += 1
                else:
                    false_positives.append((g.query, result.answer, g.expected))
        precision = correct / hits if hits else 0
        recall = hits / len(self.golden)
        return CacheEvalResult(precision, recall, hits, false_positives)

    def find_optimal_threshold(self) -> float:
        """Grid search 0.85–0.98, maximize F1 @ Precision ≥ 0.90"""
        best = 0.92
        for t in np.arange(0.85, 0.99, 0.01):
            r = self.evaluate(t)
            if r.precision >= 0.90 and r.f1 > best_f1:
                best = t
        return best
```

**Golden Set Requirements:**
- 500+ Queries pro Domain (SupportPilot: 500 FAQ + 200 Order + 100 Complaint)
- Monatliche Aktualisierung aus Production Logs (Cluster → Centroid → Human Review)
- CI Gate: Precision ≥ 0.90 @ Threshold, Recall ≥ 0.20

### 8.2 Router Evaluation

| Metrik | Target | Methode |
|--------|--------|---------|
| Intent Accuracy | ≥ 95 % | Labeled Test Set (n≥1000) |
| Calibration Error (ECE) | ≤ 0.05 | Reliability Diagram, 10 Bins |
| Conformal Coverage | ≥ 90 % | `1 - alpha` auf Holdout |
| Cost/Req vs. Baseline | ≤ 60 % | A/B: Routed vs. Single Model (Opus) |
| Fallback Rate | < 5 % | Monitoring Dashboard |

### 8.3 Budget Controller Evaluation

- **Chaos Test:** Simuliere Runaway Loop (10k req/min) → Verify Circuit Break < 30s
- **Load Test:** 10x Traffic → Verify No False Blocks (Daily Cap bei 80 %)
- **Accuracy:** Cost Estimation Error < 10 % vs. Actual Bill

### 8.4 Guardrail Evaluation

- PII Recall: ≥ 99,9 % (Presidio + Custom Patterns)
- Injection Detection: ≥ 95 % auf Benchmark (HarmBench, custom)
- Latency p99: Input ≤ 50ms, Output ≤ 50ms (Async)

---

## 9. Best Practices (Best Practices)

1. **Cache Key = Masked Query + Model Version + Tenant + Intent** — immer versioniert, immer tenant-isoliert, PII-frei
2. **Three-Tier Cache aktiv betreiben** — KV (Provider), Response (Redis), Semantic (Vector DB) — jede Tier hat eigenen Invalidation-Pfad
3. **Semantic Cache Threshold kalibrieren, nicht raten** — Golden Set, Conformal Prediction, CI Gate
4. **Router als First-Class Component** — Intent Schema versioniert, Cost pro Intent getrackt, Confidence kalibriert
5. **Budget Controller = Circuit Breaker** — Daily Hard Cap, Per-User Quota, Anomaly Detection (Z-Score), Alerting
6. **Guardrails latency-budgeted** — Input Sync Fail-Closed, Output Async Fail-Open, Gesamt ≤ 100ms
7. **PII Masking VOR Cache Write** — Key enthält masked Query, Response gespeichert masked
8. **Cache Warming aus Logs** — Nightly Job: Embed Historical Queries → Cluster → Seed Cache mit Centroid-Antworten
9. **Cost Attribution auf jedem Request** — `tenant_id, feature, model, intent, tokens_in, tokens_out, cost_usd`
10. **Observability First** — Hit-Rate pro Tier, Router Distribution, Cost/Req Trend, Budget Burn-Rate, Guardrail Latency

---

## 10. Anti-Patterns (Anti-Patterns)

| Anti-Pattern | Warum Schlecht | Besser |
|--------------|----------------|--------|
| **In-Memory Semantic Cache (List + Linear Scan)** | O(n), kein Persist, skaliert nicht >10k | pgvector/Qdrant HNSW, Hybrid BM25+Vector |
| **Hardcoded Threshold (0.92)** | Keine Domain-Anpassung, keine Evidenz | `calibrate(golden_set)`, Config-driven, CI Gate |
| **Model Snapshots in Code (`claude-sonnet-4-20250514`)** | Rottet, bricht bei Provider-Update | Generic Names + Appendix Version Table |
| **PII im Cache-Key / Response** | Cross-User Leak, Compliance-Verstoß | `redact_pii()` VOR Key-Gen + Output Re-Check |
| **Router ohne Fallback** | Classifier Fail → 500 / Wrong Model | Conformal Abstain → Embedding k-NN → Default Model → Human |
| **Budget nur als Alert (kein Block)** | Runaway kostet Geld bevor Alarm feuert | Hard Daily Cap + Circuit Breaker |
| **Guardrails nur Sync** | Output Safety blockiert User 200ms+ | Output Async, Fail-Open, Log für Review |
| **Keine Cache Invalidation bei Model Upgrade** | Stale Answers mit neuem Model-Verhalten | Versioned Keys + `invalidate_by_model_version()` Cron |
| **Cost per Call hardcoded in Router** | Pricing Drift → Falsche Routing-Entscheidung | `PricingClient` (Config/API), Versioned |
| **Semantic Cache ohne Eval** | Shippt False Positives in Produktion | Golden Set + CI Gate (Precision ≥ 0.90) |

---

## 11. Produktions-Checkliste (Production Checklist) — **NEU**

### Cache Layer
- [ ] KV-Cache aktiviert für System-Prompts ≥ 1024 Tokens (Provider-spezifisch)
- [ ] Response Cache: Redis Cluster, TTL konfiguriert, LRU Eviction getestet
- [ ] Semantic Cache: Vector DB (pgvector/Qdrant) mit HNSW Index, m/ef params dokumentiert
- [ ] Cache Keys: Versioned (model_ver), Tenant-Isolated, PII-Masked
- [ ] Invalidation: `invalidate(pattern)`, `invalidate_by_model_version()`, TTL-Jobs deployt
- [ ] Cache Stampede Protection: Redis `SET NX` oder `asyncio.Lock` pro Key
- [ ] Cache Warming: Nightly Job aus Production Logs (Cluster → Centroid → Seed)

### Semantic Cache Quality
- [ ] Golden Set ≥ 500 Queries pro Domain, monatlich aktualisiert
- [ ] Threshold kalibriert: Precision ≥ 0.90, Recall ≥ 0.20 auf Golden Set
- [ ] CI Gate: `pytest test_semantic_cache.py --threshold=0.92`
- [ ] Near-Miss Logging: Queries 0.85–0.92 Similarity für Threshold-Tuning
- [ ] Canary Deployment: Neues Embedding Model im Shadow, Hit-Rate Vergleich vor Cutover

### Semantic Router
- [ ] Intent Schema versioniert (JSON Schema), Cost/Intent definiert
- [ ] Classifier: Structured Output, gpt-4o-mini (Cost/Latency dokumentiert)
- [ ] Confidence Kalibrierung: Conformal Prediction (alpha=0.1) oder Platt Scaling
- [ ] Fallback Chain: Embedding k-NN → Default Model → Human Queue
- [ ] A/B Test Framework: Routed vs. Baseline Model aktiv
- [ ] Router Observability: Intent Distribution, Confidence Histogram, Cost/Intent

### Budget Controller
- [ ] Daily Hard Cap (z. B. 80 % Plan-Budget) mit Circuit Breaker
- [ ] Per-User Quota: RPM, TPM, $/Day konfigurierbar pro Tier
- [ ] Anomaly Detection: Z-Score > 3 auf Cost/Req → Auto-Circuit-Break
- [ ] Alerting: Webhook (Slack/PagerDuty) bei 50 %, 80 %, 100 % Budget
- [ ] Cost Attribution Tags auf JEDEM Request (Tenant, Feature, Model, Intent)

### Guardrails
- [ ] Input Guard: PII Masking (Presidio + Custom Patterns) ≤ 30ms Sync
- [ ] Input Guard: Injection Detection ≤ 20ms Sync, Fail-Closed
- [ ] Output Guard: PII Re-Check Async ≤ 50ms, Fail-Open (Log + Alert)
- [ ] Output Guard: Safety Classification Async ≤ 50ms, Fail-Open
- [ ] Gesamt Guardrail Latency Budget ≤ 100ms (p99) dokumentiert & gemessen
- [ ] Guardrail Bypass für Admin/Debug dokumentiert & auditiert

### Observability (Kap. 15 Integration)
- [ ] Dashboard: Cache Hit Rate pro Tier (KV, Response, Semantic)
- [ ] Dashboard: Router Intent Distribution, Confidence, Cost/Intent
- [ ] Dashboard: Budget Burn Rate (Daily, Per Tenant, Per Feature)
- [ ] Dashboard: Guardrail Latency p50/p95/p99, Block Rate, False Positive Rate
- [ ] Alert: Semantic Cache Precision Drop < 0.85 (Canary)
- [ ] Alert: Router Fallback Rate > 10 %
- [ ] Alert: Budget 80 % / 100 %

---

## 12. Übungen (Exercises)

| # | Titel | Schwierigkeit | Zeit | Beschreibung |
|---|-------|---------------|------|--------------|
| 1 | **Three-Tier Cache Implementieren** | ⭐⭐ | 2h | Redis Response Cache + pgvector Semantic Cache + KV-Cache Config für Anthropic/OpenAI. Unit Tests für Hit/Miss/Invalidation. |
| 2 | **Semantic Cache Eval Harness** | ⭐⭐⭐ | 3h | Golden Set (100 FAQ) laden, `SemanticCacheEvaluator` implementieren, Threshold Grid Search, CI Gate (Precision ≥ 0.90). |
| 3 | **Semantic Router mit Conformal Prediction** | ⭐⭐⭐ | 4h | Intent Classifier (gpt-4o-mini Structured Output), Conformal Calibration (alpha=0.1), Fallback Chain, A/B Test vs. Single Model. |
| 4 | **Budget Controller mit Circuit Breaker** | ⭐⭐ | 2h | Redis-backed Daily Cap + Per-User Quota + Z-Score Anomaly Detection. Chaos Test: Simuliere Runaway Loop. |
| 5 | **PII-Masking Pipeline (Pre-Cache)** | ⭐⭐ | 1.5h | Presidio + Custom Regex (IBAN, DE-Steuer-ID). Integration in Cache-Key-Gen. Output Guard Re-Check. Test: 0 Leaks auf 10k Synthetic. |
| 6 | **Guardrail Latency Budget Test** | ⭐⭐ | 1h | Locust/k6 Script: Input Guard Sync 50ms, Output Guard Async 50ms. Verify p99 < 100ms added. Fail-Open/Closed Verhaltens-Test. |
| 7 | **Cache Invalidation bei Model Upgrade** | ⭐⭐ | 1.5h | Simuliere Model Upgrade (gpt-4o-2026-03-15 → 2026-06-15). Versioned Keys + Invalidation Job. Verify keine Stale Responses. |
| 8 | **SupportPilot Mini-Capstone** | ⭐⭐⭐⭐ | 6h | End-to-End: 1k Synthetic Requests (Order/FAQ/Complaint). Three-Tier Cache + Router + Budget + Guards. Target: >50% Hit Rate, <40% Cost vs Baseline, 0 Budget Violations, 0 PII Leaks. |

---

## 13. Weiterführende Literatur (Further Reading)

### Papers & Research
- **Semantic Caching:** "GPTCache: An Open-Source Semantic Cache for LLM Applications" (Zhang et al., 2023) — arXiv:2305.06420
- **Conformal Prediction for LLM Routing:** "Conformal Prediction for Reliable LLM Routing" (Angelopoulos et al., 2024) — ICML 2024
- **Prompt Caching:** Anthropic "Prompt Caching" Docs (2024), OpenAI "Prompt Caching" Pricing (2024)
- **Vector DB Benchmarks:** "ANN Benchmarks" (Aumüller et al., ongoing) — ann-benchmarks.com
- **PII Detection:** "Presidio: Data Protection and De-identification SDK" (Microsoft, 2023)

### Tools & Libraries
- **Vector DBs:** pgvector (PostgreSQL), Qdrant, Pinecone, Weaviate, Milvus
- **Caching:** diskcache (Dev), Redis/Valkey (Prod), RedisVL (Vector + Cache)
- **Guardrails:** Microsoft Presidio, Guardrails AI, NeMo Guardrails, Lakera Guard
- **Conformal Prediction:** `conformal-prediction` (PyPI), `MAPIE` (scikit-learn compatible)
- **Observability:** Langfuse, Helicone, Datadog LLM Observability, Prometheus/Grafana

### Blog Posts & Talks
- "How We Cut LLM Costs 80% with Semantic Caching" — DoorDash Engineering (2024)
- "LLM Routing in Production" — Notion Engineering (2024)
- "Budget-Aware LLM Applications" — GitHub Copilot Blog (2024)
- "PII Redaction Before It Hits Your Vector DB" — Tonic.ai (2024)

### Standards & Compliance
- OWASP Top 10 for LLM Applications (2025) — LLM01–LLM10
- EU AI Act — Article 50 (Transparency), Annex III (High-Risk)
- GDPR Art. 25 (Data Protection by Design) — Cache Key Design

---

## Anhang: Modell-Versionstabelle (für Code-Beispiele)

| Generischer Name | Datierte Version (2026-06) | Einsatz in Kap. 12 | Quelle |
|------------------|----------------------------|-------------------|--------|
| `claude-sonnet-4` | `claude-sonnet-4-20260514` | Router: Complex Intent, Complaint | Anthropic API Docs |
| `claude-opus-4` | `claude-opus-4-20260514` | Router: Escalation/High-Stakes | Anthropic API Docs |
| `gpt-4o` | `gpt-4o-2026-03-15` | Router: Fallback, Other | OpenAI API Docs |
| `gpt-4o-mini` | `gpt-4o-mini-2026-03-15` | Router: Classifier, Simple Intent | OpenAI API Docs |
| `codestral` | `codestral-2501` | Router: Code Intent | Mistral API Docs |
| `text-embedding-3-small` | `text-embedding-3-small` (stable) | Semantic Cache, Router Embedding | OpenAI API Docs |
| `text-embedding-3-large` | `text-embedding-3-large` | RAG (Kap. 7), High-Recall Cache | OpenAI API Docs |

**Regel:** Code-Beispiele nutzen generische Namen + Config-Referenz. Anhang-Tabelle mappt auf datierte Versionen. Vierteljährlich aktualisieren.

---

## Code-Label-Konvention (für Kapitel-Autor)

| Label | Bedeutung |
|-------|-----------|
| `[Production Ready]` | Vollständig produktionsreif: Error Handling, Config-Driven, Observability Hooks, Tests |
| `[Didactic Example]` | Vereinfacht für Lernzweck: Kein Error Handling, Hardcoded Values, In-Memory Only |

**Jedes Code-Listing im Kapitel muss genau EINES dieser Labels tragen.**

---

## Querverweise & Duplikat-Vermeidung (Summary für Chapter-Writer)

| Thema | Ch 12 Behandlung | Andere Kapitel |
|-------|------------------|----------------|
| Prompt Caching (KV) | **Deep Dive** (Provider Details, Config, Invalidation) | Kap. 4: Einzeiler Forward-Ref "Details in Kap. 12" |
| Semantic Router | **Deep Home** (Implementation, Calibration, Fallback) | Kap. 3: Nur Architektur-Diagramm + Forward-Ref. TS-Code LÖSCHEN. |
| Input Guard (PII/Injection) | Integration zeigen (Router ruft Guard), Forward-Ref Kap. 16 | Kap. 16: **Canonical Implementation** (InputGuard Class) |
| Output Guard (PII/Safety) | Integration zeigen (Async, Fail-Open), Forward-Ref Kap. 16 | Kap. 16: **Canonical Implementation** (OutputGuard Class) |
| Token Budget / Cost | Runtime Budget Controller (Daily Cap, Quota, Circuit Break) | Kap. 5: Token Economics (Static). Forward-Ref "Runtime Budget in Kap. 12" |
| Model Version Pinning | Config-Driven + Appendix Table | Kap. 4: Best Practice. Ch 12 Code MUSS diesem Pattern folgen. |
| Evaluation (Cache/Router/Guards) | Eval Harness Patterns (Golden Set, Conformal, CI Gate) | Kap. 9: General Methodik. Ch 9 um "Cache/Guardrail Eval" erweitern (Empfohlen). |
| Observability | Metriken definieren (Hit-Rate, Router Dist, Budget Burn) | Kap. 15: Dashboard Implementation (Required). |

---

**Ende Outline — Bereit für Chapter-Writer Agent**