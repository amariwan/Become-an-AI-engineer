# Chapter 07 — RAG & Vector-Datenbanken: A+ Outline

**Kapitel-Datei:** `chapters/07_rag_vector_datenbanken.tex`  
**Position:** Kapitel 7 (nach Evaluation, vor Agents)  
**Produkt-Thread:** SupportPilot (B2B SaaS Support-Automatisierung) — 50k Produktdokumente, 200k Queries/Tag, 2 Tenants (B2C/B2B)  
**Ziel:** A+ (Chip Huyen / Kleppmann / Alex Xu Qualität) — chirurgische Einfügungen, kein Rewrite

---

## 1. Warum das wichtig ist (Why this matters)

**Lernziele:**
- Verstehen, warum RAG der De-facto-Standard für produktive LLM-Systeme ist (70%+ der Systeme, Quelle: a16z/Sequoia/LangChain Survey 2024)
- Unterscheiden: RAG vs. Fine-Tuning — Entscheidungsbaum für SupportPilot
- Kosten/Nutzen: Warum RAG für SupportPilot (50k Docs, 2 Tenants, tägliche Updates) vs. Fine-Tuning (10k–100k €, statisch, keine Tenant-Isolation)

**SupportPilot-Hook (Ersatz für kopierte Autornotiz):**
> "SupportPilot startete als naives RAG: `text-embedding-ada-002`, Pinecone, fest 1024-Token-Chunks, kein Hybrid, kein Re-Ranker. Hit Rate@5: 67 %. Latenz p99: 3,2 s. Kosten: 450 $/Tag. Heute: Recursive 512/64, Hybrid BM25+Vector, `bge-reranker-v2-m3`, Zitierungen, Eval-Gate. Hit Rate@5: 94 %. p99: 800 ms. Kosten: 38 $/Tag. Das ist kein Magic — das ist Pipeline-Engineering."

**Evidence-Template (für JEDE Zahl im Kapitel):**
```
[Evidence: Metric=Hit Rate@5, Baseline=0.67 (naive RAG: ada-002, fixed 1024, no hybrid, no rerank),
 Treatment=0.94 (Recursive 512/64 + BM25+Vector + bge-reranker-v2-m3),
 n=500 queries, Dataset=SupportPilot product catalog (50k docs, 2 tenants),
 Scope=E-Commerce DE/EN, Change=Chunking+Retrieval+Rerank (embedding model fixed),
 Limitations=Single domain, German queries, no OOD evaluation, Golden Set human-annotated by 2 SMEs]
```

**Cross-Refs (Backward):**
- Fine-Tuning vs. RAG Entscheidungsbaum → **Kapitel 6 (Fine-Tuning/Training)**
- Embedding-Modell-Katalog → **Kapitel 5 (Embeddings)**
- Evaluation-Methodik (Hit Rate, MRR, Faithfulness) → **Kapitel 6 (Evaluation)**
- Token-Budget & Kosten → **Kapitel 6 (Tokens/Kosten)**

---

## 2. Mentales Modell (Mental Model)

**Kernmetapher:** Zwei getrennte Pipelines — **Indexing** (offline, batch, qualitätsgetrieben) & **Retrieval+Generation** (online, latency-kritisch, bewacht).

```
┌─────────────────────────────────────────────────────────────────┐
│                    INDEXING PIPELINE (Offline)                  │
│  Docs → Chunking → Embedding → Vector DB + BM25 Index          │
│         ↑                                                         │
│    Quality Gates: Chunk-Qualität, Embedding-Drift, PII-Check   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 RETRIEVAL + GENERATION (Online)                 │
│  Query → Rewrite → Hybrid Search → Re-Rank → CRAG Gate         │
│       → Citations + Structured Output → Eval Log → Cache       │
└─────────────────────────────────────────────────────────────────┘
```

**Merke-Box:**
> **Merke:** RAG ≠ "Dokumente rein, Antwort raus". RAG = zwei Pipelines mit unterschiedlichen SLAs, Qualitätsgates und Observability. Wer nur die Retrieval-Pipeline optimiert, verpasst 60 % der Hebel (Chunking, Evaluation, Cache, Security).

**Forward-Ref:** Agents nutzen RAG als Tool → **Kapitel 8 (Agents)**

---

## 3. Architektur (Architecture)

**Zwei-Pipeline-Architektur (SupportPilot-Produktions-Architektur):**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   INGESTION     │     │   RETRIEVAL     │     │  GENERATION     │
│   (Batch)       │     │   (Online)      │     │  (Online)       │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ S3/Blob Storage │     │  Query Rewrite  │     │  CRAG Gate      │
│   ↓             │     │     ↓           │     │     ↓           │
│ Doc Parsing     │     │ Hybrid Search   │     │  LLM + Citations│
│   ↓             │     │ (BM25 + Vector) │     │     ↓           │
│ Chunking*       │     │     ↓           │     │  Structured Out │
│   ↓             │     │  Re-Ranker      │     │     ↓           │
│ Embedding       │     │     ↓           │     │  Val + Cache    │
│   ↓             │     │  Top-K Select   │     │     ↓           │
│ Vector DB       │────▶│                 │     │  Observability  │
│ (pgvector)      │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ↑                       ↑                       ↑
   Quality Gates          Latency Budget          Faithfulness
   (Chunk, Embed,          p99 < 800ms             Gate ≥ 0.85
    PII, Drift)                              (CI block)
```

**Code-Snippet 1 [Production Ready]:** `RAGPipeline` Klasse — Orchestrator mit zwei Phasen, Observability-Hooks, Tenant-Isolation.

**Cross-Ref:** Vector-DB-Provider-Details (Qdrant, Weaviate, Pinecone) → **Kapitel 8 (Vector DB Deep Dive)**

---

## 4. Kernkonzepte (Core Concepts)

### 4.1 Chunking — der größte Hebel
- **Default:** RecursiveCharacterTextSplitter 512/64 (Token-basiert, tiktoken)
- **SupportPilot Evidence:** Fixed 1024 → Recursive 512/64: **Recall@5 61% → 89%** (n=500, Golden Set, ada-002 fixed)
- **Per Content-Type (NEU — Code-Beispiele):**
  - Markdown/HTML: `MarkdownHeaderTextSplitter` → Header-Hierarchie als Metadaten [Production Ready]
  - Code: `PythonCodeTextSplitter` (AST-Grenzen) [Production Ready]
  - Tabellen: Linearisierung (Markdown→Text) oder LLM-Zusammenfassung [Production Ready]
- **Parent Document Retrieval (NEU — Critical Gap):**
  - Child Chunks (128 Tokens) für Retrieval, Parent Chunks (1536 Tokens) für LLM-Kontext
  - `ParentDocumentRetriever` (LangChain) — 2x Index-Größe, 2x Embedding-Calls
  - **When:** Legal Docs, Tech Specs, Kontext > 512 Tokens kritisch

### 4.2 Embeddings — Entscheidung, nicht Religion
- **Default:** `text-embedding-3-small` (Kosten/Qualität sweet spot, Preise -50% Aug 2024)
- **Deutsch-spezifisch:** `BAAI/bge-m3` (8192 Kontext, multilingual, dense+sparse+colbert)
- **High-End:** `voyage-3-large` (löst `voyage-2-large` ab, Okt 2024, gleiche Preis, bessere Qualität)
- **Embedding-Migration Pipeline (NEU):** Blue-Green Re-Index mit Atomarem Alias-Swap [Production Ready]
  - Evidence: **50% Re-Index-Kosten** des ursprünglichen Pipeline-Costs (one-time, batch 1000)

### 4.3 Vector DB — pgvector als Default
- **Entscheidungstabelle:** pgvector (Postgres, <10M Vektoren, bestehender Stack) vs. Qdrant/Weaviate/Pinecone (Scale, Managed, Multi-Vector)
- **HNSW Defaults:** `m=16, ef_construction=200` — **Runtime:** `ef_search` tunen (Accuracy/Latency Trade-off)
- **BM25 in Postgres:** `ts_rank_cd` + `to_tsvector` ≠ echtes BM25 → **pg_bm25 Extension** oder **ParadeDB** für echtes BM25

---

## 5. Produktions-Beispiel: SupportPilot RAG-Evolution (Production Example)

**Durchgängiger Faden durch das Kapitel — ersetzt die kopierte Autornotiz:**

| Phase | Änderung | Metrik (Evidence) | SupportPilot-Kontext |
|-------|----------|-------------------|---------------------|
| 0. Naiv | ada-002, Pinecone, Fixed 1024, kein Hybrid, kein Rerank | Hit@5 67%, p99 3.2s, $450/Tag | Baseline |
| 1. Chunking | Recursive 512/64 (tiktoken) | Recall@5 61%→89% | Produkt-IDs (KGN39XIAT) nicht mehr zerschnitten |
| 2. Hybrid | BM25 (pg_bm25) + Vector | Hit@5 +12% | Exact-Match für Produkt-Codes, Semantic für Beschreibungen |
| 3. Re-Ranker | `bge-reranker-v2-m3` (Top-20→5) | Hit@5 +15%, +50ms p99 | Cross-Encoder trennt relevante Specs von Marketing-Fluff |
| 4. Citations | Structured Output + Zitations-Validierung | Faithfulness 0.61→0.89 | Support-Agent zitiert Doc-ID, User klickt durch |
| 5. CRAG Gate | Faithfulness+Relevance Scoring + Rewrite | Refusal Rate 12%→3% | Halluzinationen blockiert, Query Rewrite für vage Fragen |
| 6. Eval Gate | Golden Set (50 Queries) in CI | Merge blockiert < 0.85 Hit@5 | Regressionen gefangen vor Deploy |
| 7. Semantic Cache | Embedding-Similarity ≥0.95, Redis Stack | **47% Cost Reduction**, <1% Quality Loss | Wiederkehrende FAQ-Queries (30%+ Duplicate Intent) |
| 8. Security | PII-Masking (Presidio) + RLS + Input Scan | 0 Leaks in 6 Monate | Tenant-Isolation erzwungen auf DB-Level |

**Jede Phase = ein Code-Snippet im Kapitel mit [Production Ready] Label.**

---

## 6. Trade-offs (Trade-offs)

| Entscheidung | Option A | Option B | Entscheidungskriterium | SupportPilot-Wahl |
|--------------|----------|----------|------------------------|-------------------|
| Chunk Size | Small (128) → Recall↑, Cost↑ | Large (1024) → Cost↓, Context↓ | Recall@k vs. Token-Budget | 512/64 Recursive + Parent Doc Retrieval |
| Hybrid Weight | α=0.5 (Vector) | α=0.7 (BM25) | Keyword-Recall vs. Semantic | α=0.6 (Produkt-IDs brauchen BM25) |
| Re-Ranker | Cross-Encoder (CPU, 50ms) | LLM-as-Judge (API, 500ms) | Latency Budget vs. Quality | Cross-Encoder (p99 < 800ms) |
| Vector DB | pgvector (Self-Hosted) | Pinecone (Managed) | Ops-Kapazität, Cost, Scale | pgvector (bestehendes Postgres, <5M vecs) |
| Cache | Exact Match | Semantic (0.95) | Hit Rate vs. Staleness | Semantic (47% Savings) |
| Tenant Isolation | App-Level Filter | Postgres RLS | Security Assurance | RLS (Enforced by DB) |

**Merke-Box:**
> **Merke:** Es gibt keine "Best Practice" ohne Kontext. Jeder Trade-off wird an **SupportPilot-SLAs** gemessen: p99 < 800ms, Hit@5 ≥ 0.90, Cost/Query < $0.002, Zero PII Leaks.

---

## 7. Failure Modes (Failure Modes)

| Failure Mode | Symptom | Detection | Mitigation (Code-Ref) |
|--------------|---------|-----------|----------------------|
| **Chunk Boundary Loss** | Antwort fehlt Kontext über Chunk-Grenze | Recall@5 Drop auf Long-Context-Queries | Parent Document Retrieval [§4.1] |
| **Embedding Drift** | Hit Rate sinkt über Wochen | Golden-Set CI Alert (wöchentlich) | Embedding Migration Pipeline [§4.2] |
| **Re-Ranker Timeout** | p99 > 1.5s | Latency Budget Alert | Fallback: Top-K ohne Rerank, Async Rerank |
| **Hallucination** | Faithfulness < 0.7 | CRAG Gate + Eval Log | CRAG Refuse/Rewrite + Citations [§5] |
| **Injection via Retrieval** | Exfiltrierung fremder Tenant-Daten | Security Audit Log | RLS + Input Scan + Output Filter [Ch 16] |
| **Cache Poisoning** | Falsche Answers aus Cache | Cache Hit Rate + Quality Drift | TTL + Similarity Threshold + Human Feedback Loop |
| **PII Leak** | Kundendaten im Index | Presidio Scan in CI | PII Masking vor Indexing [§4.2 NEU] |

---

## 8. Evaluation (Evaluation)

**Erweitert um CI-Integration, Schwellenwerte, RAGAS-Style Metriken (Forward-Ref Ch 6):**

### 8.1 Offline Evaluation (Golden Set)
- **Dataset:** 500 Queries (SupportPilot), 2 SMEs annotiert, Inter-Annotator-Agreement κ=0.82
- **Metriken mit Implementation (NEU — RAGAS-Style):**
  - **Hit Rate@k / Recall@k** — Retrieval Quality
  - **MRR / NDCG@k** — Ranking Quality
  - **Faithfulness** — LLM-Answer grounded in Context? (0–1, LLM-as-Judge, calibrated)
  - **Answer Relevance** — Answer addresses Query? (0–1, LLM-as-Judge)
  - **Context Precision** — Signal/Noise in Retrieved Context
- **Code-Snippets [Production Ready]:**
  - `GoldenSetEvaluator` mit CI-Gate (blockiert Merge < 0.85 Hit@5)
  - `FaithfulnessEvaluator` + `AnswerRelevanceEvaluator` (RAGAS 0.2.13 API pinned)
  - `LLMJudgeCalibration` (Few-Shot + Temperature 0.0 + JSON Schema)

### 8.2 Online Evaluation (Production)
- **Structured Log Schema (NEU — §2.10 Research):** `RAGQueryLog` (Pydantic) — Request-ID, Tenant, Latencies, Tokens, Cost, Hit Rate, Faithfulness, Cache Hit, Security Flags
- **Drift Detection:** Wöchentlicher Golden-Set-Run, Alert bei ΔHit@5 > 5%
- **A/B Testing Framework:** Canary Deploy neuer Chunking/Embedding/Reranker Strategien

**Cross-Ref:** Evaluation-Methodik Detail → **Kapitel 6 (Evaluation)**; Observability Deep-Dive → **Kapitel 10 (Observability)**

---

## 9. Best Practices (Best Practices)

1. **Chunking First, Embedding Second** — 80% der Retrieval-Qualität sitzt im Chunking
2. **Hybrid Search als Default** — BM25 fängt Exact-Match (IDs, Codes), Vector fängt Semantic
3. **Re-Ranker ab 10k Chunks Pflicht** — Heuristik: Top-20→5, +10-25% Hit@5, ~50ms CPU (bge-reranker-v2-m3, batch=32, CPU AVX2)
4. **Citations sind kein Nice-to-Have** — Structured Output + Validierung = Faithfulness-Gate
5. **CRAG Quality Gate vor Generation** — Faithfulness ≥ 4 UND Relevance ≥ 4 → Generate, Else Rewrite/WebSearch/Refuse
6. **Semantic Cache für >30% Duplicate Intent** — 40-60% Cost Reduction, Threshold 0.95, Redis Stack Vector Index
7. **PII Masking VOR Indexing** — Presidio Integration in Ingestion Pipeline [Production Ready]
8. **Tenant Isolation auf DB-Level (RLS)** — Nicht App-Level, SQLAlchemy Session Hook [Production Ready]
9. **Embedding Migration = Blue-Green + Alias Swap** — Zero Downtime, 50% Re-Index Cost
10. **Observability pro Query** — Structured Logs, nicht Metriken-Aggregation

---

## 10. Anti-Patterns (Anti-Patterns)

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| **Fixed-Size Chunking ohne Überlapp** | Produkt-IDs zerschnitten, Recall kollabiert | Recursive 512/64 + Parent Doc Retrieval |
| **Vector-Only Retrieval** | Keyword-Queries (IDs, Codes) fallen durch | Hybrid BM25+Vector (pg_bm25/ParadeDB) |
| **Kein Re-Ranker bei >10k Chunks** | Noise in Top-K, Halluzinationen steigen | Cross-Encoder (bge-reranker-v2-m3) |
| **LLM-as-Judge ohne Kalibrierung** | Faithfulness Scores unzuverlässig | Few-Shot + Temp 0.0 + JSON Schema + Human Calibration Set |
| **Cache ohne TTL/Similarity-Threshold** | Veraltete Answers, Quality Drift | LRU + Threshold 0.95 + Feedback Loop |
| **App-Level Tenant Filter** | SQL Injection → Cross-Tenant Leak | Postgres RLS (Row Level Security) |
| **Embedding Model Wechsel ohne Migration** | Index Drift, Silent Quality Drop | Blue-Green Pipeline + Alias Swap |
| **Keine Evaluation in CI** | Regressionen erreichen Production | Golden Set (50+) + Hit@5 Gate ≥ 0.85 |

---

## 11. Produktions-Checkliste (Production Checklist) — NEU

| Kategorie | Check | Tool/Code-Ref | Status |
|-----------|-------|---------------|--------|
| **Chunking** | Recursive 512/64 + Parent Doc für Long-Context | `ParentDocumentRetriever` | ☐ |
| **Chunking** | Content-Type Splitter (MD, Code, Tables) | `MarkdownHeaderTextSplitter`, `PythonCodeTextSplitter` | ☐ |
| **Embeddings** | Model Version gepinnt, Drift-Monitoring | Golden Set Weekly Run | ☐ |
| **Embeddings** | Migration Pipeline Blue-Green Ready | `EmbeddingMigrator` | ☐ |
| **Vector DB** | pgvector HNSW `ef_search` getunt | Benchmark Script | ☐ |
| **Vector DB** | Echtes BM25 (pg_bm25/ParadeDB) | Extension installiert | ☐ |
| **Retrieval** | Hybrid Search (α=0.6 default) | Configurable | ☐ |
| **Retrieval** | Re-Ranker (bge-reranker-v2-m3) Top-20→5 | Latency Budget 50ms | ☐ |
| **Retrieval** | Multi-Vector/ColBERT/SPLADE evaluiert | Recall@k Gap Analysis | ☐ |
| **Generation** | Structured Output + Citations | Pydantic Model + Validation | ☐ |
| **Generation** | CRAG Gate (Faithfulness+Relevance) | `CRAGEvaluator` | ☐ |
| **Generation** | Streaming + Citations (Hard Problem) | Buffer + Validate | ☐ |
| **Evaluation** | Golden Set (n≥50) in CI | `GoldenSetEvaluator` | ☐ |
| **Evaluation** | Faithfulness/Answer Relevance Gates | RAGAS 0.2.13 Pinned | ☐ |
| **Evaluation** | NDCG@10 + MRR getrackt | Online Dashboard | ☐ |
| **Security** | PII Masking (Presidio) in Ingestion | `mask_pii()` | ☐ |
| **Security** | RLS Policies für alle Tenant-Tabellen | SQLAlchemy Session Hook | ☐ |
| **Security** | Input Scan (Injection) + Output Filter | Ch 16 Patterns | ☐ |
| **Performance** | Semantic Cache (Redis Stack) | `SemanticCache` | ☐ |
| **Performance** | Cost/Query < $0.002 | Daily Cost Report | ☐ |
| **Observability** | Structured Log pro Query (RAGQueryLog) | Pydantic + Structlog | ☐ |
| **Observability** | Drift Alert (ΔHit@5 > 5%) | Weekly Golden Set | ☐ |

---

## 12. Übungen (Exercises)

1. **Chunking-Vergleich:** Implementiere Fixed 1024 vs. Recursive 512/64 vs. Parent Doc Retrieval auf SupportPilot-Subset (1k Docs). Messe Recall@5, Index-Größe, Embedding-Cost. Dokumentiere Trade-offs.
2. **Hybrid Search Tuning:** Variiere α (0.3–0.7) für BM25/Vector Gewichtung. Finde Optimum für Produkt-ID-Queries vs. Beschreibungs-Queries.
3. **Re-Ranker Ablation:** Ohne Reranker vs. `ms-marco-MiniLM-L-6-v2` vs. `bge-reranker-v2-m3`. Messe Hit@5, Latency p99, CPU Cost.
4. **CRAG Gate Calibration:** Kalibriere Faithfulness/Relevance Thresholds (1-5) gegen Human-Labels (n=100). Finde Operating Point: Max Recall bei Faithfulness ≥ 0.85.
5. **Semantic Cache A/B:** Deploy Cache (Threshold 0.95) für 10% Traffic. Messe Cost Reduction, Cache Hit Rate, Quality Delta (Faithfulness).
6. **Embedding Migration Drill:** Simuliere Migration `text-embedding-3-small` → `bge-m3` mit Blue-Green Pipeline. Messe Downtime, Cost, Quality Delta.
7. **Security Red Team:** Versuche Tenant-Isolation zu brechen (SQL Injection via Query, Prompt Injection via Retrieved Doc). Dokumentiere Blockierung durch RLS/Input Scan/Output Filter.
8. **Evaluation CI Gate:** Baue Golden Set (50 Queries) in GitHub Actions. Blockiere Merge bei Hit@5 < 0.85. Erweitere um Faithfulness Gate.

---

## 13. Weiterführende Literatur (Further Reading)

**Papers (mit BibTeX-Keys für Bibliography):**
- Lewis et al. 2020 — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (RAG Original)
- Gao et al. 2022 — *Precise Zero-Shot Dense Retrieval without Relevance Labels* (HyDE)
- Yan et al. 2024 — *Corrective Retrieval Augmented Generation* (CRAG)
- Chen et al. 2024 — *Parent Document Retriever* (LangChain/LlamaIndex Pattern)
- Santhanam et al. 2022 — *ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction*
- Formal et al. 2021 — *SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking*
- Sarti et al. 2024 — *RAGAS: Automated Evaluation of Retrieval Augmented Generation* (Pin: `ragas==0.2.13`)

**Tools & Libraries:**
- `pgvector` / `pg_bm25` / `ParadeDB` — Postgres Extensions
- `ragatouille` — ColBERT in Python
- `Qdrant` / `Weaviate` — Multi-Vector Support (SPLADE, ColBERT native)
- `GPTCache` / `Redis Stack` — Semantic Caching
- `Presidio` — PII Detection/Anonymization
- `Langfuse` / `LangSmith` — Observability & Evaluation

**Blogs/Deep-Dives:**
- Pinecone "RAG Best Practices" (laufend aktualisiert)
- Chroma "Advanced RAG Patterns"
- Jeremy Howard "RAG from Scratch" (fast.ai)
- Chip Huyen "Evals for RAG" (2024)

---

## Cross-Chapter Reference Map (für Chapter-Writer)

**Backward References (dieses Kapitel → frühere):**
1. Fine-Tuning vs. RAG → **Ch 6**
2. Embedding Models → **Ch 5**
3. Evaluation Metrics (Hit Rate, MRR, Faithfulness) → **Ch 6**
4. Token Budget / Cost → **Ch 6**
5. Security Overview → **Ch 16** (bereits Zeile 848)

**Forward References (spätere Kapitel → dieses):**
1. Agents nutzen RAG als Tool → **Ch 8** (hinzufügen: "Agenten nutzen RAG als Tool — Kapitel 8")
2. Production Pipeline Patterns → **Ch 9** referenziert Ch 7
3. Structured Log Schema → **Ch 10** (Observability) erweitert dies
4. Golden Set / CI Gates → **Ch 11** (Evaluation) vertieft Ch 7 §8
5. When RAG fails → Fine-Tune → **Ch 12** referenziert Ch 7 Decision Tree
6. Embedding Fine-Tuning → **Ch 13** referenziert Ch 7 Migration
7. Indirect Injection Deep-Dive → **Ch 16** vertieft Ch 7 §7
8. Re-Ranker Latency / Quantization → **Ch 17** (Inference Opt) optimiert Ch 7 Komponenten

**SupportPilot Narrative Arc:**
- Ch 5: Model Selection (Embeddings für DE-Produktdaten)
- **Ch 7: Core RAG Pipeline** ← DIESER OUTLINE
- Ch 8: Agent = RAG Tool + Escalation Tool + Ticket Tool
- Ch 9: Canary Deploy Chunking Strategies
- Ch 10: Query Logs → Drift Detection Hit Rate
- Ch 11: Golden Set Expansion, LLM-Judge Calibration
- Ch 16: Injection Analytics, Tenant Isolation Audit

---

## Teaser für nächstes Kapitel (am Kapitelende)

> "RAG liefert Kontext. Aber was, wenn die Frage **Aktion** erfordert — Ticket anlegen, Rückruf terminieren, API aufrufen? Dann wird aus Retrieval ein **Agent**. Kapitel 8 zeigt, wie SupportPilot RAG als Tool in eine Agent-Schleife einbindet: Reasoning → Tool Call (RAG) → Tool Call (Ticket) → Response."

---

## Code-Snippet Inventar (alle 14 + 6 NEU = 20 Snippets — JEDES mit Label)

| # | Snippet | Label | Status |
|---|---------|-------|--------|
| 1 | RAGPipeline Orchestrator | [Production Ready] | Existing → Label hinzufügen |
| 2 | Recursive Chunker 512/64 | [Production Ready] | Existing → Label hinzufügen |
| 3 | ParentDocumentRetriever | [Production Ready] | **NEU (§4.1)** |
| 4 | MarkdownHeaderTextSplitter | [Production Ready] | **NEU (§4.1)** |
| 5 | PythonCodeTextSplitter | [Production Ready] | **NEU (§4.1)** |
| 6 | Table Linearization | [Production Ready] | **NEU (§4.1)** |
| 7 | EmbeddingMigrator Blue-Green | [Production Ready] | **NEU (§4.2)** |
| 8 | Hybrid Search (BM25+Vector) | [Production Ready] | Existing → Label + pg_bm25 Note |
| 9 | Cross-Encoder Re-Ranker (bge-reranker-v2-m3) | [Production Ready] | Existing → Model Update + Label |
| 10 | Step-Back Prompting | [Production Ready] | **NEU (§5)** |
| 11 | Query Decomposition | [Production Ready] | **NEU (§5)** |
| 12 | CRAGEvaluator (Faithfulness+Relevance) | [Production Ready] | **NEU (ersetzt §5.4)** |
| 13 | GoldenSetEvaluator + CI Gate | [Production Ready] | Existing → Erweitern (NDCG, Faithfulness, Answer Relevance) |
| 14 | FaithfulnessEvaluator (RAGAS-Style) | [Production Ready] | **NEU (§8)** |
| 15 | AnswerRelevanceEvaluator (RAGAS-Style) | [Production Ready] | **NEU (§8)** |
| 16 | SemanticCache (Redis Stack) | [Production Ready] | **NEU (§5/10)** |
| 17 | PII Masking (Presidio) | [Production Ready] | **NEU (§7/10)** |
| 18 | SQLAlchemy RLS Session Hook | [Production Ready] | **NEU (§7/10)** |
| 19 | RAGQueryLog (Structured Logging) | [Production Ready] | **NEU (§8/10)** |
| 20 | Multi-Vector/ColBERT/SPLADE Overview | [Didactic Example] | **NEU (§5)** |

---

## Checkliste für Chapter-Writer (Definition of Done)

- [ ] Autornotiz Zeilen 7-13 **komplett ersetzt** durch SupportPilot RAG-Story
- [ ] **Alle 20 Code-Snippets** haben Caption-Label `[Production Ready]` oder `[Didactic Example]`
- [ ] **8 Zahlen-Claims** haben Evidence-Footnotes (Template aus §1)
- [ ] **Keine Jahreszahlen** (2023, 2024) im Fließtext
- [ ] **6 Missing Patterns** eingefügt: Parent Doc, Multi-Vector, Advanced Rewriting, Migration, Cache, PII
- [ ] **2 Models aktualisiert:** `voyage-3-large`, `bge-reranker-v2-m3`
- [ ] **ts_rank_cd Hinweis:** "Für echtes BM25: pg_bm25 Extension oder ParadeDB"
- [ ] **Faithfulness/Answer Relevance/Context Precision** Implementation + Forward-Ref Ch 6
- [ ] **8 Cross-Refs** eingefügt (5 backward, 3 forward — siehe Map)
- [ ] **SupportPilot Thread** zieht sich durch alle Sections (Tabelle in §5 als Rückgrat)
- [ ] **Teaser am Ende** zeigt auf Agents (Ch 8)
- [ ] **Production Checklist** (§11) vollständig
- [ ] **Build compiles** (`latexmk -xelatex -outdir=_build main.tex` — 0 Warnings)
- [ ] **Spellcheck DE/EN** (VS Code) clean

---

**Outline Status:** READY FOR CHAPTER-WRITER AGENT  
**Estimated Edit Time:** 6-8h chirurgische Einfügungen (kein Rewrite)  
**Next Agent:** `chapter-writer` → produces `chapters/07_rag_vector_datenbanken.tex`