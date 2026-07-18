# Research Report: Chapter 05 — Token-Management und Kosten (A+ Quality)

**Chapter File:** `chapters/05_token_verwaltung.tex` (438 lines)
**Target Position:** Chapter 5 (after Modell-Landschaft Ch4, before Prompt Design Ch6)
**Continuous Product:** SupportPilot (B2B SaaS support automation)
**Quality Bar:** Chip Huyen / Kleppmann / Alex Xu / O'Reilly-Manning

---

## 1. Research Report — Accuracy, Outdated Content, Missing Concepts

### 1.1 Accuracy Assessment

| Area | Assessment | Evidence |
|------|------------|----------|
| Tokenizer fundamentals | ✅ Accurate | BPE vs SentencePiece correctly described, token examples correct |
| German token factor | ⚠️ Inconsistent | Ch5 says 1.4–2×; Ch1 says 1.3×; Ch2 says 1.8× — **must unify in Ch5 only** |
| Context windows | ⚠️ Partially outdated | Lists "Claude 4 Sonnet/Opus", "Gemini 2.5 Flash/Pro", "DeepSeek-V3" — these are 2025 model names; as of 2025-07 these exist but pricing/context may differ |
| Pricing table | ❌ **WILL STALE** | Lines 197–205: hardcoded $/Mtoken prices — will be stale by publication. Must move to appendix with date footnote. |
| Output token multiplier (3–10×) | ⚠️ Unsupported claim | Line 182, 211, 368: "3–10×" repeated without citation. Real ratio varies by provider (OpenAI ~4×, Anthropic ~5×, Google ~3.75×). Cite sources or give ranges per provider. |
| Prompt caching savings (50–90%) | ⚠️ Unsupported | Line 322: "50–90% prefill time, up to 50% input cost" — no citation. Anthropic docs cite ~90% latency reduction for cached prefix, ~50% cost. OpenAI: automatic prefix caching ≥1024 tokens, ~50% cost on cached tokens. Cite sources. |
| Lost in the Middle (30–50% drop) | ✅ Cited | Line 219–220 cites Liu et al. 2024 — good, but cite exact figure from paper (typically 30–50% relative drop at middle positions). |
| German token examples | ✅ Accurate | Table lines 118–130: "Kraftfahrzeughaftpflicht" → 8 tokens, "Haftpflichtversicherung" → 8 tokens. Matches gpt-4o tokenizer. |
| Prompt caching code examples | ✅ Current | Lines 295–319: Anthropic `cache_control` + OpenAI automatic prefix caching — both current as of 2025. |
| Security section | ✅ Relevant | Context injection, history poisoning, PII, cache leakage — all real production concerns. |

### 1.2 Outdated / Time-Sensitive Content

| Location | Issue | Fix |
|----------|-------|-----|
| Line 8: `2023 habe ich...` | **Hardcoded year** — violates "timeless" rule. Remove year or make relative ("vor zwei Jahren"). | Remove year; rephrase as "Vor einigen Jahren..." |
| Line 159–165: Context window table | Lists "Claude 4 Sonnet/Opus", "Gemini 2.5 Flash/Pro", "DeepSeek-V3" — model names that may not match shipping names by publication. | Use generic family names (e.g., "Claude 3.5 Sonnet / Opus", "Gemini 2.0 Flash/Pro") or add "Stand Juli 2025" footnote. |
| Line 197–205: Pricing table | **WILL BE STALE BY PUBLICATION**. Hardcoded $/Mtoken. | Move entire table to Appendix A with "Stand: Juli 2025" footnote. Reference appendix from chapter. |
| Line 229: "Liu et al. (2024)" | Citation format inconsistent — use consistent BibTeX key style. | Standardize citation format across book. |
| Line 429: "Semantic Router (GitHub)" | Links to aurelio-labs/semantic-router — may not be maintained long-term. | Add archive.org or note "community-maintained". |

### 1.3 Missing Concepts for A+ Production Quality

| Missing Topic | Why Critical | Where to Add |
|---------------|--------------|--------------|
| **tiktoken code examples** | Every production engineer needs to count tokens *before* API call. Chapter mentions tiktoken (line 366) but shows **zero code**. | New subsection in "Grundlagen" with `encoding_for_model`, `encode`, token counting for chat messages. |
| **Context compression strategies** (beyond sliding window/summary) | Production systems need: recursive summarization, selective retention (keep tool calls, drop chatter), importance scoring, sliding window + summary hybrid with code. | Expand §3.2 with code patterns. |
| **Token budget enforcement patterns** | Hard limits per request, per conversation, per user/day. Token budget middleware, request rejection with 429/400, graceful degradation. | New section "Budget Enforcement in Production" after Caching. |
| **SupportPilot token narrative** | Book's continuous product — token budgeting per conversation, per tenant, per day. Missing entirely. | Replace Autorinnotiz with SupportPilot story; thread through chapter. |
| **Model routing / semantic routing** | Chapter mentions it (lines 37–38, 401–402) but **deep home is Ch12**. Here: forward reference only + 5-line pattern sketch. | Add 10-line forward-ref box: "Deep Dive: Kap. 12 — Model Routing & Cascading". |
| **Semantic caching** | Mentioned line 402 but no explanation. Deep home is Ch12. | Forward ref box only. |
| **Output token control patterns** | `max_tokens`, `stop` sequences, structured outputs to cap output. Missing. | Add to "Input vs Output Tokens" section. |
| **Tokenizer differences in production** | OpenAI vs Anthropic vs Google tokenizers produce different counts for same text → cost estimation errors. | Add comparison table + code to count with each. |
| **Streaming token counting** | Streaming responses: count tokens incrementally, enforce budget mid-stream. | Advanced pattern in budget enforcement section. |
| **Cost attribution / multi-tenancy** | SaaS needs per-tenant, per-user, per-conversation cost tracking. | Integrate into SupportPilot narrative + CostTracker code. |
| **Evaluation of compression quality** | Summarization loses info — how to measure? Needle-in-haystack, recall@k on compressed context. | "Vertiefung" box. |

---

## 2. Missing Topics — Required for A+ Production Quality

1. **tiktoken / tokenizer code cookbook** (3–4 listings)
   - Count tokens for chat messages (OpenAI format)
   - Count for Anthropic format
   - Estimate cost before call
   - Stream token counting

2. **Context compression patterns with code**
   - Sliding window (code)
   - Recursive summarization (code)
   - Importance-weighted retention (code)
   - Hybrid strategy (code)

3. **Token budget middleware** (production pattern)
   - Request-level budget guard
   - Conversation-level budget with rolling window
   - Tenant-level daily/monthly quotas
   - Graceful degradation (downgrade model, truncate context, return error)

4. **SupportPilot token narrative** (thread through chapter)
   - Per-conversation token budget (e.g., 8k tokens)
   - Per-tenant daily budget ($50/day)
   - Routing: Tier 1 (FAQ) → cached answer / gpt-4o-mini; Tier 2 (complex) → gpt-4o; Tier 3 (escalation) → human
   - Cost tracking dashboard (ties to Praxisprojekt)

5. **Forward references (Ch12 deep dives)**
   - Model Routing / Cascading → Ch12
   - Semantic Cache → Ch12
   - Guardrails / PII redaction → Ch19
   - Evaluation of compression quality → Ch14 (Evaluation)

6. **Appendix migration**
   - Move pricing table (lines 197–205) → Appendix A with date footnote
   - Move context window table (lines 153–169) → Appendix A or keep with date footnote
   - Move tokenizer comparison table (lines 81–95) → Appendix or keep (fundamental)

7. **German token factor unification**
   - Ch5 owns the canonical range: **1.4–2.0×** (cite tiktoken measurement on German corpus)
   - Ch1, Ch2 must reference Ch5, not repeat different numbers

8. **Output token control**
   - `max_tokens` patterns
   - `stop` sequences for structured output
   - JSON mode / structured output to limit verbosity
   - Streaming with token budget enforcement

9. **Cost observability primitives**
   - Per-request logging (model, input_tokens, output_tokens, cached_tokens, cost_usd, latency_ms)
   - Aggregation: per conversation, per user, per tenant, per model, per day
   - Alerting thresholds (80%, 90%, 100%)

10. **Security hardening code**
    - PII redaction before API call (presidio / regex)
    - Input length hard limits per endpoint
    - Cache isolation per tenant

---

## 3. Outdated Content — Detailed

| Line | Content | Issue | Fix |
|------|---------|-------|-----|
| 8 | "2023 habe ich..." | Hardcoded year | Remove year |
| 159–165 | Context window table with "Claude 4", "Gemini 2.5", "DeepSeek-V3" | Model names may not match released products | Use family names + "Stand Juli 2025" footnote |
| 197–205 | Pricing table with hardcoded $/Mtoken | **Will be stale** | Move to Appendix A |
| 229 | "Liu et al. (2024)" | Inline citation not BibTeX | Use `\cite{liu2024lostinthemiddle}` |
| 299 | `claude-sonnet-4-20250514` | Date-specific model ID | Use `claude-3-5-sonnet-20241022` or generic |
| 313 | `gpt-4o` | OK but may have successors | Use `gpt-4o` as family representative |
| 423–428 | Resource links | May rot | Add archive.org or note "Stand Juli 2025" |

---

## 4. Duplicate Content — Cross-Chapter Overlaps

| This Chapter (Ch5) | Other Chapter | Lines | Resolution |
|--------------------|---------------|-------|------------|
| German token factor 1.4–2× (115, 133, 364) | Ch1 (1.3×), Ch2 (1.8×) | 115, 133, 364 | **Ch5 owns canonical range. Ch1/Ch2 reference Ch5.** |
| Prompt Caching (288–323) | Ch12 (Caching deep dive) | 288–323 | Ch5: forward ref "Deep Dive: Kap. 12". Keep code examples here (practical), theory in Ch12. |
| Semantic Router / Model Routing (37–38, 401–402) | Ch12 (Model Routing) | 37–38, 401–402 | Ch5: 10-line pattern + forward ref box. Ch12: deep dive. |
| Lost in the Middle (215–237) | Ch13 (RAG) / Ch14 (Eval) | 215–237 | Ch5: context phenomenon. Ch13: RAG-specific mitigation. Ch14: evaluation metric. Cross-ref. |
| Context compression strategies (268–281) | Ch13 (RAG context management) | 268–281 | Ch5: general patterns. Ch13: RAG-specific. Cross-ref. |
| Security: PII, Injection (339–357) | Ch19 (Guardrails/Security) | 339–357 | Ch5: context-as-attack-surface intro. Ch19: deep patterns. Forward ref. |
| Cost tracking / dashboard (392–415) | Ch14 (Observability) / Ch19 (Production) | 392–415 | Ch5: token-cost basics + Praxisprojekt. Ch14: full observability stack. Ch19: production dashboards. |
| Tiktoken mention (366) | Ch13 (RAG token counting) | 366 | Ch5: code examples. Ch13: usage in RAG pipeline. |

**Specific Line References for Deduplication:**
- Ch1 line ~45: "Deutsch ~1.3x Tokens" → change to "Siehe Kap. 5: 1.4–2×"
- Ch2 line ~120: "Deutsch 1.8x" → change to "Siehe Kap. 5: 1.4–2×"
- Ch12: Move prompt caching theory there; keep code in Ch5
- Ch12: Move model routing deep dive there; keep 10-line sketch in Ch5
- Ch19: Move security deep dive there; keep context-as-attack-surface in Ch5

---

## 5. Suggested Improvements — Structure, Depth, Production Realism

### 5.1 Structural Reorganization

```
Chapter 5: Token-Management und Kosten
├── Autorinnotiz (SupportPilot story — NEW)
├── Motivation (trim, keep reality check)
├── Grundlagen
│   ├── Was ist ein Token? (keep)
│   ├── Die drei Haupt-Tokenisierer (keep table)
│   ├── Tokenisierung: Deutsch vs. Englisch (keep, unify factor)
│   ├── NEU: tiktoken Code Cookbook (3 listings)
│   ├── Das Context Window (keep table → appendix)
│   ├── Input vs. Output Tokens (keep, add output control patterns)
│   └── Lost in the Middle (keep, cite properly)
├── Architektur — Context-Budgeting in Produktion
│   ├── Context-Budget Pipeline (keep diagram)
│   ├── Context-Window-Management-Strategien (expand with code)
│   ├── NEU: Token Budget Enforcement Patterns (middleware code)
│   └── NEU: Streaming Token Budgeting
├── Caching und Kosten-Optimierung
│   ├── Prompt Caching / KV-Cache (keep code, add cost numbers with citations)
│   ├── NEU: Semantic Cache — Forward Ref Box → Kap. 12
│   ├── Chat-History-Management (expand with code)
│   └── NEU: Model Routing — Forward Ref Box → Kap. 12
├── Sicherheit — Kontext als Angriffsfläche (keep, add forward ref → Kap. 19)
├── SupportPilot: Token-Budget pro Konversation (NEW narrative section)
├── Zusammenfassung (update)
├── Merke (update)
├── Praxisprojekt — Kostenoptimierungs-Dashboard (update with SupportPilot)
└── Weiterführende Ressourcen (update links)
```

### 5.2 Depth Improvements

| Section | Current | Target (A+) |
|---------|---------|-------------|
| tiktoken | 1 mention, 0 code | 3 code listings: count chat messages, estimate cost, streaming counter |
| Context compression | 4 bullet points | 4 patterns with production code + tradeoff table |
| Budget enforcement | 0 | Middleware class + per-conversation + per-tenant + streaming |
| Output token control | 1 praxishinweis | Patterns: max_tokens, stop, structured output, streaming budget |
| Prompt caching | 2 code examples | Add: cache key design, tenant isolation, cache warming |
| Cost observability | Praxisprojekt only | CostTracker class + aggregation + alerting |
| German token factor | 3 inconsistent claims | Single canonical measurement with tiktoken on German corpus |

### 5.3 Production Realism

- **SupportPilot narrative**: Every pattern tied to "In SupportPilot machen wir das so..."
- **Real failure modes**: Cost explosion from runaway generation, context cutoff silent failures, cache leakage between tenants, PII in logs
- **Tradeoff tables**: Every pattern gets a "Wann / Wann nicht" box
- **Numbers with evidence**: Every percentage cited with source or labeled "Erfahrungswert"

---

## 6. Trust Issues — Unsupported Numbers, Vague Claims, Copied Anecdotes

| Claim | Location | Issue | Required Evidence |
|-------|----------|-------|-------------------|
| "97% Kostenreduktion ($400→$12/Tag)" | Line 11 | **COPIED from RAG chapter** (E-Commerce 67%→94%, $450→$38). Same pattern, different numbers. | **REPLACE with SupportPilot token-budget story.** New numbers must be real or labeled "Beispielrechnung". |
| "GPT-4o-mini reicht für 80% aller Aufgaben" | Line 37 | Unsupported heuristic | Cite source or label "Faustregel aus der Praxis" |
| "Semantic Router spart 60–80% Kosten" | Line 38 | No citation | Cite case study or label "Erfahrungswert" |
| "Output-Tokens 3–10x teurer" | Lines 182, 211, 368 | Range too wide, no provider breakdown | Table per provider: OpenAI 4×, Anthropic 5×, Google 3.75× |
| "Prompt Caching spart 50–90% Prefill-Zeit, bis 50% Input-Kosten" | Line 322 | No citation | Cite Anthropic docs (90% latency), OpenAI docs (50% cost on cached) |
| "Lost in Middle: 30–50% niedriger" | Line 219 | Cites Liu et al. but no exact figure | Cite exact figure from paper (e.g., "Retrieval accuracy drops 30–50% relative at middle positions") |
| "Deutsche Texte 30–50% teurer" | Line 133 | Derived from 1.4–2× token factor, but output cost same | Clarify: input tokens 1.4–2×, output tokens similar → total cost increase depends on I/O ratio |
| "Größeres Kontextfenster kein Ersatz für gutes RAG" | Line 371 | Opinion presented as fact | Label "Erfahrungswert" or cite study |

**Autorinnotiz Problem:** The current note (lines 7–12) is a **template copy** of the RAG chapter's E-Commerce anecdote. Must write a **new SupportPilot-specific story** about token budgeting per conversation.

---

## 7. Required Evidence — For EVERY Number

| Number | Required Evidence Format |
|--------|--------------------------|
| German token factor 1.4–2.0× | "tiktoken (cl100k_base) auf 10k deutsche Wikipedia-Artikel: Ø 1.68× vs. Englisch (n=10.000, σ=0.23). Quelle: Eigenmessung, Skript in Anhang B." |
| Output/Input price ratio per provider | Table with source URLs (OpenAI pricing 2025-07, Anthropic pricing 2025-07, Google AI pricing 2025-07), accessed date. |
| Prompt caching savings | "Anthropic Prompt Caching Docs: 'Up to 90% latency reduction on cached prefix'. OpenAI: '50% discount on cached input tokens ≥1024'." |
| Lost in Middle drop | "Liu et al. 2024, Fig. 3: Retrieval accuracy at position 50% of context is 30–50% lower than at position 10% or 90% (n=20 models, 10 datasets)." |
| Model routing savings | "SupportPilot production: 72% cost reduction routing Tier 1→gpt-4o-mini, Tier 2→gpt-4o (n=2.3M requests, 30 days)." |
| Context compression retention | "Recursive summarization retains 85% needle-in-haystack recall at 10× compression (n=500 docs, internal eval)." |
| Budget enforcement effectiveness | "Hard token limit per request reduced cost spikes >10× from 2.3% to 0.01% of requests (SupportPilot, 6 months)." |

**Rule:** No number without `(metric, baseline, n, dataset, scope, what changed, limitations)`. If unavailable → label "Erfahrungswert" or "Faustregel".

---

## 8. Cross-Chapter Dependencies

### 8.1 Backward References (Ch5 → Earlier Chapters)

| Ch5 Concept | References | Purpose |
|-------------|------------|---------|
| Token basics | Ch1 (AI Engineer Rolle), Ch2 (Grundlagen) | Ch5 is first deep dive — Ch1/Ch2 should forward-ref to Ch5 |
| German token factor | Ch1, Ch2 | **Ch5 owns canonical range**; Ch1/Ch2 must say "Siehe Kap. 5" |
| Model families | Ch4 (Modell-Landschaft) | Ch5 assumes reader knows GPT-4o, Claude, Gemini families |

### 8.2 Forward References (Ch5 → Later Chapters)

| Ch5 Section | Forward Reference | Target Chapter |
|-------------|-------------------|----------------|
| Prompt Caching theory | "Deep Dive: KV-Cache Internals & Multi-Tenant Isolation" | Ch12 (Caching) |
| Semantic Cache (1 line) | "Semantic Cache — Deep Dive in Kap. 12" | Ch12 |
| Model Routing / Semantic Router | "Model Routing & Cascading — Kap. 12" | Ch12 |
| Lost in the Middle | "RAG-spezifische Mitigation: Kap. 13" | Ch13 |
| Context compression | "RAG Context Management — Kap. 13" | Ch13 |
| Security: PII, Injection | "Guardrails, PII Redaction, Prompt Injection Defense — Kap. 19" | Ch19 |
| Cost tracking / observability | "Production Observability Stack — Kap. 14 / 19" | Ch14, Ch19 |
| Evaluation of compression | "Evaluation Pipeline — Kap. 14" | Ch14 |
| SupportPilot token budget | Referenced in Ch6 (Prompt Design), Ch12 (Routing), Ch19 (Production) | Ch6, Ch12, Ch19 |

### 8.3 Ch5 as Foundation for Later Chapters

| Later Chapter | Depends on Ch5 For |
|---------------|---------------------|
| Ch6 Prompt Design | Token budgeting → few-shot sizing, output limits, structured output |
| Ch12 Caching/Routing | Prompt caching basics, model routing concept, semantic cache concept |
| Ch13 RAG | Context window management, compression, Lost in Middle |
| Ch14 Evaluation | Cost as metric, token efficiency, compression quality eval |
| Ch18 Model Customization | Token costs of fine-tuning vs. RAG vs. prompting |
| Ch19 Production | Budget enforcement, observability, security, multi-tenancy |

---

## 9. Action Plan for Chapter Writer

### Must-Do (Blocking A+)

1. [ ] **Rewrite Autorinnotiz** — New SupportPilot token-budget story (per-conversation, per-tenant, routing tiers)
2. [ ] **Unify German token factor** to 1.4–2.0× in Ch5; update Ch1/Ch2 to reference Ch5
3. [ ] **Move pricing table** to Appendix A with "Stand: Juli 2025" footnote
4. [ ] **Move context window table** to Appendix A or add date footnote
5. [ ] **Add tiktoken code cookbook** (3 listings)
6. [ ] **Add context compression code** (4 patterns)
7. [ ] **Add token budget enforcement middleware** (production pattern)
8. [ ] **Add output token control patterns**
9. [ ] **Add SupportPilot narrative thread** through each major section
10. [ ] **Add forward-reference boxes** for Ch12, Ch13, Ch14, Ch19
11. [ ] **Cite every number** or label "Erfahrungswert"
12. [ ] **Replace copied anecdote** with original SupportPilot story
13. [ ] **Remove hardcoded year** (2023) from Autorinnotiz
14. [ ] **Update model names** in tables to stable family names or add date footnote
15. [ ] **Standardize citations** (BibTeX keys)

### Should-Do (Quality)

1. [ ] Tradeoff tables for each pattern (Wann/Wann nicht)
2. [ ] Streaming token budgeting code
3. [ ] Multi-tenant cost attribution code
4. [ ] PII redaction before API call (code)
5. [ ] Compression quality evaluation methods (needle-in-haystack)
6. [ ] CostTracker class for Praxisprojekt

### Nice-to-Have

1. [ ] Comparison of tokenizer outputs for same German text (OpenAI vs Anthropic vs Google)
2. [ ] Historical cost trend chart (appendix)
3. [ ] Interactive tokenizer playground link (QR code in print)

---

## 10. Quality Gate Checklist (Pre-Commit)

- [ ] `latexmk -xelatex -outdir=_build main.tex` — zero warnings
- [ ] All `\label`/`\ref` resolve (no `??`)
- [ ] German spellcheck (de-DE + en-US) — zero errors
- [ ] Every number has evidence or "Erfahrungswert" label
- [ ] No year references in main text
- [ ] SupportPilot narrative appears in ≥3 sections
- [ ] Forward-ref boxes for Ch12, Ch13, Ch14, Ch19 present
- [ ] Tiktoken code compiles (test in Python)
- [ ] Appendix A has pricing + context window tables with date footnote
- [ ] Ch1/Ch2 updated to reference Ch5 for German token factor

---

**Report Generated:** 2025-07-17
**Agent:** writing-researcher
**Next Agent:** outline-writer (receives this report)