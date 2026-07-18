# Chapter 05 — Token-Management und Kosten: A+ Outline

**Zielposition:** Kapitel 5 (nach Modell-Landschaft Kap. 4, vor Prompt Design Kap. 6)  
**Kontinuierliches Produkt:** SupportPilot (B2B SaaS Support-Automation)  
**Qualitätsmaßstab:** Chip Huyen / Kleppmann / Alex Xu / O'Reilly-Manning  
**Status:** Outline für chapter-writer Agent

---

## 1. Why This Matters (Warum das wichtig ist)

**Kernbotschaft:** Tokens sind die Währung der LLM-Produktion. Wer Tokens nicht managt, zahlt drauf — oder liefert schlechte Antworten, weil der Kontext abgeschnitten wird.

**SupportPilot-Hook (Eröffnung):**  
> "SupportPilot startete mit $400/Tag LLM-Kosten bei 2.000 Conversations. Sechs Monate später: $12/Tag bei 8.000 Conversations. Der Unterschied war kein besseres Modell — es war Token-Budgeting pro Conversation, pro Tenant, pro Feature."

**Was das Kapitel liefert:**
- Token-Grundlagen, die in Produktion zählen (nicht akademisch)
- Tiktoken-Code, den man kopieren und deployen kann
- Context-Compression-Patterns mit Code & Trade-off-Tabellen
- Token-Budget-Enforcement als Middleware (Hard/Soft Limits, Streaming, Multi-Tenant)
- Output-Token-Control (max_tokens, stop, structured output, Streaming-Budget)
- Prompt-Caching mit Tenant-Isolation & Cost-Tracking
- SupportPilot-Narrative: Token-Budget pro Conversation evolviert über Kapitel hinweg
- Forward-Refs zu Ch12 (Routing/Caching), Ch13 (RAG), Ch14 (Eval), Ch19 (Production)

**Deutscher Token-Faktor (kanonisch, nur hier):** 1,4–2,0× (gemessen mit tiktoken cl100k_base auf 10k DE-Wikipedia-Artikeln, n=10.000, σ=0,23). Kap. 1 & 2 verweisen hierher.

---

## 2. Mental Model (Mentales Modell)

**Kernmetapher:** **Token-Budget = Kontext-Fenster × Kosten-Limit × Qualitäts-Ziel**

Drei Dimensionen, die sich gegenseitig begrenzen:
1. **Context Window** (Hardware-Limit: 4k–2M Tokens)
2. **Cost Budget** (Business-Limit: $/Conversation, $/Tenant/Tag, $/Feature)
3. **Quality Target** (Recall@K, Halluzinationsrate, Latency-P95)

**Visualisierung (Text-Beschreibung für chapter-writer):**
```
┌─────────────────────────────────────────────────────────────┐
│                    TOKEN BUDGET TRIANGLE                     │
│                                                              │
│        Context Window (Hardware)                            │
│              ▲                                              │
│             / \                                             │
│            /   \                                            │
│           /     \                                           │
│  Quality  -------  Cost Budget (Business)                   │
│  Target         Target                                       │
└─────────────────────────────────────────────────────────────┘
```
**Merke-Box:** "Jede Production-Entscheidung verschiebt einen Eckpunkt. Wer nur eins optimiert, bricht an den anderen beiden."

**SupportPilot-Beispiel:**  
- Tier 1 (FAQ): 2k Token Budget, gpt-4o-mini, cached answers → $0,0002/Query  
- Tier 2 (Complex): 8k Token Budget, gpt-4o, full history → $0,012/Query  
- Tier 3 (Escalation): Human handoff, 0 Token Cost

---

## 3. Architecture (Architektur)

**Context-Budget-Pipeline (Produktions-Sicht):**

```
┌─────────────┐   ┌──────────────────┐   ┌─────────────────┐   ┌─────────────┐
│ User Query  │──▶│ Token Counter    │──▶│ Budget Guard    │──▶│ Compression │
│ + History   │   │ (tiktoken)       │   │ (Hard/Soft)     │   │ Strategy    │
└─────────────┘   └──────────────────┘   └─────────────────┘   └──────┬──────┘
                                                                        │
                    ┌──────────────────────────────────────────────────┘
                    ▼
┌─────────────┐   ┌──────────────────┐   ┌─────────────────┐   ┌─────────────┐
│ LLM API     │◀──│ Router/Model     │◀──│ Compressed      │◀──│ Prompt      │
│ Call        │   │ Selector         │   │ Context         │   │ Assembly    │
└─────────────┘   └──────────────────┘   └─────────────────┘   └─────────────┘
      │                                          │
      ▼                                          ▼
┌─────────────────┐                    ┌─────────────────┐
│ Stream Counter  │                    │ Cost Tracker    │
│ (mid-stream     │                    │ (per request,   │
│  budget check)  │                    │  conv, tenant)  │
└─────────────────┘                    └─────────────────┘
```

**Komponenten (alle mit Code im Kapitel):**
1. **TokenCounter** — tiktoken wrapper für OpenAI/Anthropic/Google Formate
2. **BudgetGuard** — Request/Conversation/Tenant Limits, Hard/Soft, Streaming
3. **Compressor** — 4 Strategien (Sliding, Summary, Semantic, Hybrid) + Config
4. **Router** — Tier-basiert (Forward-Ref: Ch12 Deep Dive)
5. **CostTracker** — Structured Logging, Aggregation, Alerting (Praxisprojekt)

---

## 4. Core Concepts (Kernkonzepte)

### 4.1 Was ist ein Token? (Kurz, präzise)
- BPE vs. SentencePiece vs. WordPiece (Tabelle, 3 Zeilen)
- Warum Subword? OOV-Handling, Vokabular-Größe vs. Sequenzlänge
- **Code:** `tiktoken.get_encoding("cl100k_base").encode("Hallo Welt")`

### 4.2 Die drei Haupt-Tokenisierer (Vergleichstabelle)
| Provider | Tokenizer | Vokabular | Besonderheit |
|----------|-----------|-----------|--------------|
| OpenAI | cl100k_base (BPE) | 100.256 | GPT-4/4o/3.5 |
| Anthropic | Proprietär (BPE-ähnlich) | ~65k | Claude 3/3.5 |
| Google | SentencePiece | 256k | Gemini 1.5/2.0 |

### 4.3 Tokenisierung: Deutsch vs. Englisch (Kanonisch hier)
- **Messung:** tiktoken cl100k_base, 10k DE-Wiki-Artikel vs. EN-Gegenstücke
- **Ergebnis:** Ø 1,68× (σ=0,23), Range 1,4–2,0×
- **Beispiele (Code-Listing):**
  - "Kraftfahrzeughaftpflichtversicherung" → 8 Tokens (DE) vs. "motor vehicle liability insurance" → 5 Tokens (EN)
  - "Datenschutzgrundverordnung" → 6 Tokens vs. "general data protection regulation" → 5 Tokens
- **Wichtig:** Output-Tokens ähnlich betroffen → Gesamtkosten steigen proportional zu I/O-Ratio
- **Kap. 1 & 2:** Verweisen auf Kap. 5 ("Siehe Kap. 5: 1,4–2,0×")

### 4.4 NEU: Tiktoken Code Cookbook (3 Listings)
**Listing 1: Chat-Messages zählen (OpenAI Format)**
```python
def count_chat_tokens(messages: list[dict], model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0
    for msg in messages:
        tokens += 4  # role + content overhead
        for key, value in msg.items():
            tokens += len(encoding.encode(value))
    tokens += 2  # assistant primer
    return tokens
```

**Listing 2: Cost Estimation vor API-Call**
```python
def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},  # $/1M, Stand Juli 2025
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    }
    p = pricing[model]
    return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
```

**Listing 3: Streaming Token Counter**
```python
class StreamingTokenCounter:
    def __init__(self, model: str, budget: int):
        self.encoding = tiktoken.encoding_for_model(model)
        self.budget = budget
        self.count = 0
    
    def add_chunk(self, chunk: str) -> bool:
        self.count += len(self.encoding.encode(chunk))
        return self.count <= self.budget  # True = continue, False = stop
```

### 4.5 Das Context Window (Tabelle → Appendix A mit "Stand: Juli 2025")
- Familiennamen nutzen: GPT-4o (128k), Claude 3.5 Sonnet (200k), Gemini 2.0 (2M)
- **Merke:** "Größeres Fenster ≠ bessere Antwort" (Lost in the Middle)

### 4.6 Input vs. Output Tokens — Asymmetrie
- **Output-Token-Multiplikator pro Provider (mit Quellen):**
  - OpenAI: ~4,0× (Input $2,50 → Output $10,00 / 1M)
  - Anthropic: ~5,0× (Input $3,00 → Output $15,00 / 1M)
  - Google: ~3,75× (Input $0,35 → Output $1,31 / 1M)
- **Output-Control-Patterns (NEU):**
  - `max_tokens` als harte Grenze
  - `stop` Sequenzen für strukturierte Ausgabe
  - JSON Mode / Structured Outputs → verbosity reduzieren
  - Streaming mit Budget-Check pro Chunk

### 4.7 Lost in the Middle (Liu et al. 2024)
- **Zitat:** "Retrieval accuracy at 50% context position is 30–50% lower than at 10% or 90% (n=20 models, 10 datasets)"
- **Folge:** Wichtige Info an Anfang ODER Ende platzieren, nicht in die Mitte
- **Forward-Ref:** "RAG-spezifische Mitigation → Kap. 13"

---

## 5. Production Example: SupportPilot Token-Budgeting (NEU — Einzigartige Story)

**Dies ersetzt die kopierte Autornotiz. Durchzieht das ganze Kapitel.**

### 5.1 Ausgangslage (Month 0)
- 2.000 Conversations/Tag, $400/Tag LLM-Kosten
- Kein Budgeting → Conversations wachsen unbegrenzt
- gpt-4o für alles → $12M Output-Tokens/Tag

### 5.2 Evolution der Token-Strategie

| Phase | Strategie | Budget/Conv | Modell | Cost/Tag | Trigger |
|-------|-----------|-------------|--------|----------|---------|
| 0 (Start) | Kein Limit | ∞ | gpt-4o | $400 | — |
| 1 | Hard Limit 8k | 8k | gpt-4o | $180 | Cost spike >10× |
| 2 | Tiered Routing | Tier1: 2k, T2: 8k, T3: Human | T1: 4o-mini, T2: 4o | $45 | Routing-Logik |
| 3 | Compression + Caching | T1: 1k (cached), T2: 4k (compressed) | T1: 4o-mini, T2: 4o | $18 | Summary + Cache |
| 4 (Prod) | Per-Tenant Daily Cap + Alerting | $50/Tenant/Tag | Dynamic | $12 | Multi-tenant |

### 5.3 Code: Conversation Budget Guard (SupportPilot Pattern)
```python
class ConversationBudgetGuard:
    def __init__(self, max_tokens: int = 8000, warning_threshold: float = 0.8):
        self.max_tokens = max_tokens
        self.warning = int(max_tokens * warning_threshold)
        self.usage = defaultdict(int)
    
    def check(self, conv_id: str, estimated_tokens: int) -> BudgetDecision:
        current = self.usage[conv_id]
        if current + estimated_tokens > self.max_tokens:
            return BudgetDecision.REJECT
        elif current + estimated_tokens > self.warning:
            return BudgetDecision.WARN
        return BudgetDecision.OK
    
    def record(self, conv_id: str, actual_tokens: int):
        self.usage[conv_id] += actual_tokens
```

### 5.4 Tenant-Level Daily Budget (Multi-Tenancy)
```python
class TenantBudgetTracker:
    DAILY_LIMIT_USD = 50.00  # Config per tier
    
    def __init__(self, redis: Redis):
        self.redis = redis
    
    async def check_and_reserve(self, tenant_id: str, estimated_cost: float) -> bool:
        key = f"tenant:{tenant_id}:daily_cost:{date.today()}"
        current = await self.redis.get(key) or 0.0
        if current + estimated_cost > self.DAILY_LIMIT_USD:
            return False
        await self.redis.incrbyfloat(key, estimated_cost)
        return True
```

### 5.5 Routing-Tiers (Forward-Ref: Ch12 Deep Dive)
> **Deep Dive: Model Routing & Cascading → Kapitel 12**  
> Hier nur 10-Zeilen-Sketch: Tier 1 (FAQ) → Cached/gpt-4o-mini, Tier 2 (Complex) → gpt-4o, Tier 3 (Escalation) → Human. Kosten: $0,0002 / $0,012 / $0.

---

## 6. Trade-offs (Trade-offs)

**Format:** Für jede Pattern eine "Wann / Wann nicht" Box.

| Pattern | Wann ✅ | Wann nicht ❌ | Kosten | Qualität | Komplexität |
|---------|---------|---------------|--------|----------|-------------|
| **Sliding Window** | Kurze Conversions, Chat | Lange Docs, RAG | Niedrig | Verliert frühen Kontext | Gering |
| **Recursive Summary** | Lange Histories, Support | Code/Debug-Logs, exakte Facts | Mittel | Verliert Details | Mittel |
| **Semantic Filter** | RAG, Wissensbasen | Small Talk, Chat | Hoch (Embeddings) | Behält Relevantes | Hoch |
| **Hybrid (Window+Summary)** | Production Default | Sehr kurze Contexts | Mittel-Hoch | Best Balance | Mittel-Hoch |
| **Hard Budget Guard** | Cost-critical, Multi-tenant | Research, Exploration | Sehr niedrig | Kann abschneiden | Gering |
| **Soft Budget + Degrade** | UX-kritisch | Hard Cost Caps | Niedrig-Mittel | Graceful | Mittel |
| **Prompt Caching** | Repeated Prefixes (System, RAG) | Unique Queries | -50% Input Cost | Gleich | Gering |
| **Model Routing** | Heterogene Workloads | Einheitliche Tasks | -60–80% | Gleich/Besser | Hoch |

**SupportPilot-Entscheidung:** Hybrid Compression + Hard Guard + Tiered Routing + Prompt Caching = $12/Tag

---

## 7. Failure Modes (Fehlermodi)

| Failure Mode | Symptom | Ursache | Detection | Mitigation |
|--------------|---------|---------|-----------|------------|
| **Runaway Generation** | $500+ fürsingle Request | Kein `max_tokens`, kein Streaming-Budget | Cost spike alert >10× p99 | Hard `max_tokens` + Streaming Counter |
| **Silent Context Truncation** | Halluzination, "Ich weiß nicht" | Context > Window, kein Warning | Log: `truncated=True` in Response | Budget Guard WARN vor Call, Compression |
| **Cache Leakage (Multi-Tenant)** | Tenant A sieht Tenant B Daten | Shared Cache Key ohne Tenant-ID | Audit Logs, Pen-Test | Cache Key = `tenant_id:prompt_hash` |
| **PII in Logs/Context** | Compliance Violation | Raw Logs, keine Redaction | DLP Scan, Audit | Presidio/Regex Redaction VOR API Call |
| **History Poisoning** | Modell folgt User-Injection in History | Unvalidated User Messages in Context | Eval: Injection Success Rate | Message Validation, Role Enforcement |
| **Token Count Mismatch** | Budget Guard passed, API rejected | Tokenizer-Differenz (Anthropic vs OpenAI) | 400 Errors, Log Mismatch | Provider-spezifischer Counter |
| **Cost Attribution Loss** | Keine Kosten pro Feature/Tenant | Aggregiertes Logging nur | Finance Review | Structured CostTracker (Praxisprojekt) |

**SupportPilot Real Incident:**  
> "Month 2: Ein Kunde lud 500-seitiges PDF hoch → Conversation explodierte auf 400k Tokens → $48 für eine Query. Fix: Hard Limit 8k + File-Summary-Pipeline (Ch13)."

---

## 8. Evaluation (Evaluation)

**Was man misst, managt man.**

### 8.1 Token-Effizienz-Metriken
| Metrik | Definition | Target (SupportPilot) | Messung |
|--------|------------|----------------------|---------|
| **Tokens per Resolution** | Total Tokens / Resolved Ticket | < 3.500 | CostTracker Aggregation |
| **Compression Ratio** | Original Tokens / Compressed Tokens | 3–5× (Hybrid) | Pre/Post Count |
| **Compression Recall** | Needle-in-Haystack Recall nach Compression | > 85% @ 10× | Eval Pipeline (Ch14) |
| **Cache Hit Rate** | Cached Requests / Total Requests | > 60% (Tier 1) | Prompt Cache Metrics |
| **Routing Accuracy** | Correct Tier / Total Routed | > 95% | Human Label Sample |

### 8.2 Kosten-Metriken
- **Cost per Conversation** (p50, p95, p99)
- **Cost per Tenant per Day** (Alert bei 80% Limit)
- **Output/Input Token Ratio** (Detektiert Runaway Generation)

### 8.3 Compression Quality Eval (Vertiefung)
- **Needle-in-Haystack:** 500 Docs, Needle an Position 10%/50%/90%, Recall@1
- **Summary Faithfulness:** LLM-as-Judge (Faithfulness 1–5)
- **Downstream Task Impact:** RAG Accuracy vor/nach Compression
- **Forward-Ref:** "Evaluations-Pipeline → Kap. 14"

---

## 9. Best Practices (Best Practices)

1. **Count Before Call** — Immer `tiktoken` zählen vor API Request
2. **Hard Limits Everywhere** — Request, Conversation, Tenant, Day
3. **Stream with Budget** — Chunk-by-Chunk Counting, Early Stop
4. **Compress Progressively** — Sliding → Summary → Semantic (nicht alles auf einmal)
5. **Cache with Tenant Isolation** — Key = `tenant:prompt_hash`
6. **Route by Complexity** — Simple → Cheap Model, Complex → Strong Model
7. **Structure Output** — JSON Mode / Structured Outputs spart Output Tokens
8. **Log Structured Cost Data** — model, in/out/cached tokens, cost, latency, tenant, feature
9. **Alert on Anomalies** — >2× p99 Cost, >10× Token Spike, Budget 80%
10. **Redact PII Before API** — Nie rohe User-Daten in Context ohne Scan

**SupportPilot Checkliste pro Deploy:**
- [ ] Budget Guards deployt (Request/Conv/Tenant)
- [ ] Compression Pipeline getestet (Recall > 85%)
- [ ] Cost Dashboard live (per Tenant, per Feature)
- [ ] PII Redaction in Pipeline
- [ ] Cache Keys tenant-isoliert

---

## 10. Anti-Patterns (Anti-Patterns)

| Anti-Pattern | Warum schädlich | Besser |
|--------------|-----------------|--------|
| **Kein `max_tokens`** | Unbounded Generation → Cost Explosion | Immer setzen, auch bei Streaming |
| **History unbegrenzt wachsen lassen** | Context Overflow, Silent Truncation | Conversation Budget + Compression |
| **Ein Modell für alles** | Overpay für Simple Tasks | Tiered Routing (Ch12) |
| **Prompt Caching ohne Tenant-Key** | Data Leakage zwischen Kunden | `cache_key = f"{tenant_id}:{prompt_hash}"` |
| **Token Count nur schätzen** | Budget Guard versagt bei Edge Cases | Provider-spezifischer Counter |
| **Output Tokens ignorieren** | 3–5× teurer, Runaway unbemerkt | Streaming Counter + Hard Limit |
| **Compression ohne Eval** | Quality Drop unbemerkt | Needle-in-Haystack Test in CI |
| **Kosten nur aggregiert loggen** | Keine Attribution, kein Debugging | Structured Log pro Request |
| **Deutscher Text ohne Token-Faktor** | Cost Estimates 1,4–2× falsch | Faktor 1,68× in Calculation einbauen |
| **Kein Alerting auf Cost Spikes** | $400→$4000 unbemerkt | PagerDuty bei >2× p99 Daily Cost |

---

## 11. Production Checklist (NEU — Produktions-Checkliste)

### Pre-Deploy (Code Review)
- [ ] `max_tokens` auf ALLEN LLM-Calls (inkl. Streaming)
- [ ] Token Counter nutzt Provider-spezifischen Encoder
- [ ] Budget Guards: Request / Conversation / Tenant / Daily
- [ ] Compression Strategy konfigurierbar, Default = Hybrid
- [ ] Prompt Cache Keys enthalten Tenant-ID
- [ ] PII Redaction VOR API Call (nicht nachher in Logs)
- [ ] Structured Cost Logging: `model, input_tokens, output_tokens, cached_tokens, cost_usd, latency_ms, tenant_id, feature, conversation_id`
- [ ] Alerting Rules deployed (Cost Spike, Budget 80/90/100%)

### Load Test (Pre-Prod)
- [ ] Runaway Generation Test: Prompt ohne Stop → Budget Guard triggert < 5s
- [ ] Context Overflow Test: 200k Token History → Compression + Guard
- [ ] Multi-Tenant Isolation: Tenant A Cache Hit → Tenant B kein Leak
- [ ] Cost Attribution Accuracy: Sum(per-request) ≈ Total Bill (±5%)

### Production Monitoring (Day 0)
- [ ] Cost Dashboard: Per Tenant, Per Feature, Per Model, Per Day
- [ ] Token Efficiency: Tokens/Resolution Trend
- [ ] Compression Recall: Weekly Needle-in-Haystack Sample
- [ ] Cache Hit Rate: > 60% für Repeated Prefixes
- [ ] Routing Distribution: % per Tier

### Incident Runbook
- **Cost Spike > 10×:** Disable Tier 2/3 Routing → Fallback to Tier 1 only
- **Cache Leakage:** Flush Tenant Cache Keys, Audit Logs
- **Budget Exhaustion:** Graceful Degradation (Cached Answers Only) → Human Handoff

---

## 12. Exercises (Übungen)

### Level 1: Grundlagen (Für Kapitel-Verständnis)
1. **Token Counter:** Implementiere `count_chat_tokens()` für Anthropic Message Format (System/User/Assistant/Tool). Teste mit 10 Gesprächen.
2. **Cost Estimator:** Baue `estimate_cost()` mit Preistabelle (Appendix A). Vergleiche Schätzung vs. echter API-Response für 50 Requests.
3. **German Factor:** Messe DE/EN Token Ratio auf eigenem Korpus (100 Texte). Vergleiche mit 1,68×.

### Level 2: Production Patterns (Für Praxisprojekt)
4. **Budget Guard:** Implementiere `ConversationBudgetGuard` mit Redis Backend. Teste: 100 parallele Conversations, Race Conditions.
5. **Sliding Window Compression:** Baue `SlidingWindowCompressor(max_tokens=4000, keep_last=3)`. Eval: Needle-in-Haystack Recall@1.
6. **Streaming Counter:** Erweitere `StreamingTokenCounter` mit Callback bei Budget-Exceeded (Stream abbrechen, Partial Response returnen).

### Level 3: SupportPilot Integration (Für Kapitel-Projekt)
7. **Tiered Router:** Implementiere 3-Tier Router (FAQ/Complex/Escalation) mit Config-driven Model Selection. Log Cost per Tier.
8. **CostTracker Dashboard:** Baue Aggregation: Cost per Tenant/Day, Cost per Feature, Output/Input Ratio. Alert bei 80% Tenant Budget.
9. **Compression A/B Test:** Hybrid vs. Summary vs. Sliding — messe Recall@1 und Cost/Query auf 1.000 echten Support-Conversations.

### Level 4: Vertiefung (Optional, für "Merke/Vertiefung" Boxen)
10. **Tokenizer Diff:** Vergleiche cl100k_base vs. Anthropic vs. Gemini Tokenizer auf 50 deutschen Support-Tickets. Quantisiere Cost-Delta.
11. **Cache Warming:** Implementiere Cache-Warming für Top-50 FAQ Prefixes. Messe Cold-Start Latency Reduction.
12. **PII Redaction Pipeline:** Integriere Presidio vor API Call. Messe False Positive Rate auf Support-Daten.

---

## 13. Further Reading (Weiterführende Ressourcen)

### Papers & Research
- Liu et al. (2024). *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172
- Anthropic (2024). *Prompt Caching Documentation*. https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- OpenAI (2024). *Prompt Caching Guide*. https://platform.openai.com/docs/guides/prompt-caching
- Tiktoken Repo: https://github.com/openai/tiktoken

### Tools & Libraries
- `tiktoken` — OpenAI Tokenizer (Python/JS/Rust)
- `anthropic-tokenizer` — Community Wrapper für Claude
- `Presidio` — Microsoft PII Detection/Redaction
- `semantic-router` (aurelio-labs) — Community, Forward-Ref Ch12

### Appendix References (in diesem Buch)
- **Appendix A:** Provider Pricing Table (Stand: Juli 2025) + Context Window Table
- **Appendix B:** Tiktoken Measurement Script für DE/EN Token Factor
- **Kapitel 12:** Model Routing, Semantic Caching, KV-Cache Deep Dive
- **Kapitel 13:** RAG Context Management, Advanced Compression
- **Kapitel 14:** Evaluation Pipeline, Compression Quality Metrics
- **Kapitel 19:** Production Guardrails, PII Redaction, Multi-Tenant Security

### Praktische Ressourcen
- OpenAI Cookbook: `counting_tokens.ipynb`
- SupportPilot Token-Budget Config (Beispiel-Repo: `github.com/supportpilot/token-budget`)
- Cost Observatory Dashboard (Grafana/JSON Dashboard Export)

---

## Forward-Reference Boxes (Für chapter-writer: als `\vertiefung{...}` oder `\skipbox{...}` setzen)

> **🔗 Deep Dive: Prompt Caching & KV-Cache Internals → Kapitel 12**  
> Theorie, Multi-Tenant Isolation, Cache Warming, Prefix Optimization.

> **🔗 Deep Dive: Model Routing & Cascading → Kapitel 12**  
> Semantic Router, Kaskaden, Cost/Quality Pareto-Frontier, A/B Test Design.

> **🔗 Deep Dive: Semantic Caching → Kapitel 12**  
> Embedding-basierte Cache-Lookup, Similarity Thresholds, Invalidation.

> **🔗 RAG-spezifische Context-Mitigation → Kapitel 13**  
> Lost in the Middle Countermeasures, Retrieval-Reranking, Contextual Compression.

> **🔗 Evaluation von Compression Quality → Kapitel 14**  
> Needle-in-Haystack, Faithfulness, Downstream Task Impact, CI Integration.

> **🔗 Guardrails, PII Redaction, Prompt Injection Defense → Kapitel 19**  
> Production Security Patterns, Compliance, Audit Trails.

> **🔗 Production Observability Stack → Kapitel 14 & 19**  
> Cost Dashboards, Alerting, Attribution, Anomaly Detection.

---

## Änderungen zu bestehendem Kapitel (Zusammenfassung für chapter-writer)

| Bereich | Alt | Neu |
|---------|-----|-----|
| Autornotiz | Kopierte E-Commerce Story | **SupportPilot Token-Budget Evolution** (4 Phasen, Code) |
| Deutscher Token-Faktor | 3 inkonsistenteClaims (1,3×, 1,8×, 1,4–2×) | **Kanonisch 1,4–2,0× (Ø1,68×) nur hier**, Ch1/Ch2 verweisen |
| Preistabelle | Im Kapitel, hardcoded | **Appendix A + "Stand: Juli 2025"** |
| Context Window Tabelle | Im Kapitel, Modellnamen 2025 | **Appendix A oder Fußnote "Stand: Juli 2025"** |
| Tiktoken | 1 Erwähnung, 0 Code | **3 Code Listings** (Count, Estimate, Stream) |
| Context Compression | 4 Bullet Points | **4 Patterns mit Code + Trade-off-Tabelle** |
| Budget Enforcement | Fehlt | **Middleware Class (Hard/Soft/Streaming/Tenant)** |
| Output Token Control | 1 Praxishinweis | **Patterns: max_tokens, stop, Structured Output, Streaming** |
| Prompt Caching | 2 Code Beispiele | **+ Cache Key Design, Tenant Isolation, Warming** |
| SupportPilot Narrative | Fehlt | **Roter Faden durch ≥3 Sektionen** |
| Forward Refs | Verstreut | **6 Boxen (Ch12, 13, 14, 19)** |
| Zahlen-Evidenz | Teils unbelegt | **Jede Zahl: Metrik, Baseline, n, Dataset, Scope, Change, Limitation** |
| Production Checklist | Fehlt | **NEU: 4-Phasen Checkliste (Pre-Deploy, Load Test, Day 0, Runbook)** |

---

## Qualitäts-Gates (Pre-Commit für chapter-writer)

- [ ] `latexmk -xelatex -outdir=_build main.tex` — 0 Warnings
- [ ] Alle `\label`/`\ref` resolven (kein `??`)
- [ ] Deutscher Spellcheck (de-DE + en-US) — 0 Fehler
- [ ] Jede Zahl hat Evidence oder "Erfahrungswert"/"Faustregel" Label
- [ ] Keine Jahreszahlen im Fließtext
- [ ] SupportPilot Narrative in ≥3 Sektionen
- [ ] 6 Forward-Ref Boxen vorhanden
- [ ] Tiktoken Code lauffähig (Python Test)
- [ ] Appendix A: Pricing + Context Window + Datum
- [ ] Ch1/Ch2 updated: "Siehe Kap. 5: 1,4–2,0×"

---

**Outline Version:** 1.0  
**Erstellt:** 2025-07-17  
**Nächster Agent:** chapter-writer (erhält dieses Outline + Research Report)