# Chapter 11 Outline: Inference-Optimierung und Serving (A+ Target)

**Chapter File:** `chapters/11_inferenz_optimierung.tex`  
**Book Position:** Chapter 11 (nach Ch 10 Caching, vor Ch 12/13 Fine-Tuning)  
**Product Context:** SupportPilot (B2B SaaS Support-Automation, PII-sensitiv)  
**Tone:** Senior Developer — direkt, ehrlich, praxisnah, keine akademischen Füllwörter  
**Language:** Deutsch (babel `german`)  
**Code Labels:** Jedes Snippet mit `[Production Ready]` oder `[Didactic Example]` markiert

---

## 1. Why This Matters (Motivation)

**Kernthese:** Wer LLMs in Produktion selbst hostet (Compliance, Kosten, Kontrolle), scheitert nicht an Modellqualität — sondern an Inference-Engineering: TTFT, Durchsatz, GPU-Auslastung, Cold Starts.

**SupportPilot Hook (1 Absatz):**
- B2B SaaS, Support-Tickets enthalten PII (E-Mail, Order-ID, Stacktraces)
- DSGVO/Enterprise-Verträge verbieten OpenAI/Anthropic API
- Lösung: Self-Host Llama-3.1-70B auf 4×A100 80GB
- Ohne Optimierung: 45% GPU-Util, 2.1s TTFT p95, $3.600/Monat Hardware
- Mit Optimierung (Kapitel 11): 2×A100, 78% Util, 1.1s TTFT, 6× Durchsatz, $1.800/Monat vs. GPT-4o API $8.500

**Skip Box (NEU, nach Motivation):**
```latex
\skipbox{
\bfseries Überspringen, wenn: Du nutzt nur API-Modelle (OpenAI, Anthropic, Gemini) und hast 
keine PII-Compliance-Anforderungen oder Volumen >10.000 Requests/Tag. 
Dieses Kapitel behandelt Self-Hosting-Optimierung (vLLM, Quantisierung, Speculative Decoding). 
Für API-Nutzung lies Kapitel 18 (Routing) und 19 (Guardrails).
}
```

**Lernziele (3–4 Bulletpoints):**
- Prefill/Decode-Phasen unterscheiden und Engpässe identifizieren
- vLLM (PagedAttention, Continuous Batching, Prefix Caching) produktiv betreiben
- Quantisierung (AWQ/FP8) mit Qualitätsregression messen, nicht raten
- Speculative Decoding nur einsetzen, wenn Acceptance Rate >60%
- Benchmark-Methodik anwenden, die Zahlen reproduzierbar macht

**Cross-Refs:**
- `\ref{chap:caching}` — Prompt Caching Strategien (Ch 10)
- `\ref{chap:evaluation}` — Golden Dataset für Qualitätsvalidierung (Ch 9)
- `\ref{chap:ai_engineer_rolle}` — Cost Awareness (Ch 1)

---

## 2. Mental Model

**Zwei-Phasen-Modell (Prefill vs. Decode):**
- **Prefill:** Parallel, compute-bound, Input-Token → KV-Cache füllen. Batch-Size = 1 bei Chat, >1 bei Batch-Inference.
- **Decode:** Sequentiell, memory-bound, Token-für-Token, KV-Cache lesen. Batch-Size = gleichzeitige Requests.

**Fünf Engpässe (Tabelle, verfeinert aus Research):**

| Engpass | Phase | Symptom | Hebel |
|---------|-------|---------|-------|
| Compute (Prefill) | Prefill | Hohe TTFT, GPU-Compute <80% | Chunked Prefill, FlashAttention-2, TP |
| Memory Bandwidth (Decode) | Decode | Hohe TPOT, GPU-Memory <60% | Quantisierung (INT4/FP8), SpecDec, KV-Cache Offload |
| KV-Cache Fragmentierung | Decode | OOM bei langen Contexts, schwankende TPOT | PagedAttention (vLLM Standard), Prefix Caching |
| Scheduler Overhead | Beide | Geringe Util bei kleinen Batches | Continuous Batching, In-Flight Batching (TRT-LLM) |
| Cold Start / Model Load | Startup | 30–120s bis erster Token | Model Pinning, Pre-warm, Eager Mode |

**Merke-Box:**
```latex
\merke{
Prefill = „Wie lange bis zum ersten Token?“ (TTFT). Decode = „Wie schnell die nächsten Token?“ (TPOT). 
Optimierung beginnt immer mit Messen: Welche Phase limitiert DEINEN Use-Case?
}
```

**Cross-Ref:** Ch 17 (Production) für Autoscaling basierend auf diesen Metriken.

---

## 3. Architecture

**High-Level Serving Stack (Text + ASCII-Diagramm):**

```
┌─────────────────────────────────────────────────────────────┐
│                    Client / Gateway                         │
│              (Auth, Rate Limit, Routing)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────▼─────────────┐
        │     Load Balancer         │
        │   (Round Robin / Least    │
        │    Connections / Prefix   │
        │    Affinity für Cache)    │
        └─────────────┬─────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐       ┌─────▼─────┐     ┌─────▼─────┐
│ vLLM  │       │ vLLM      │     │ vLLM      │  ← Replica Set (TP=4)
│ Worker│       │ Worker    │     │ Worker    │
└───┬───┘       └─────┬─────┘     └─────┬─────┘
    │                 │                 │
    └─────────────────┼─────────────────┘
                      │
        ┌─────────────▼─────────────┐
        │    Monitoring Stack       │
        │  (Prometheus, Grafana,    │
        │   DCGM Exporter, Logs)    │
        └───────────────────────────┘
```

**Drei Deployment-Optionen (Vergleichstabelle):**

| Kriterium | vLLM (Open Source) | TensorRT-LLM (NVIDIA) | Triton Inference Server |
|-----------|-------------------|----------------------|------------------------|
| **Stärke** | Flexibel, Python-native, Community | Max Perf auf NVIDIA HW, FP8, PP | Model Orchestration, Ensembles, A/B |
| **Schwäche** | Kein PP, Python GIL bei Pre/Post | Engine Build nötig, weniger flexibel | Komplexer Setup, Overhead |
| **Best For** | Iteration, Custom Logic, Multi-LoRA | H100/Blackwell Max-Throughput | Multi-Model, Reranker+LLM, Versioning |
| **SupportPilot Wahl** | ✅ Hauptserving | Evaluation für H100 Migration | Für Ensemble (Classifier + LLM) |

**Cross-Refs:**
- `\ref{chap:finetuning}` — Multi-LoRA Serving auf gemeinsamer Basis (Ch 13)
- `\ref{chap:routing}` — Router: Einfache Tickets → 3B, Komplex → 70B (Ch 18)
- `\ref{chap:production}` — K8s Deployment, Autoscaling (Ch 17)

---

## 4. Core Concepts

### 4.1 PagedAttention (vLLM Kern)
- Problem: Klassisches KV-Cache = kontiguier Blöcke → Fragmentierung, OOM
- Lösung: PagedAttention — KV-Cache in fixen Pages (z.B. 16 Token), virtuelle → physische Mapping
- Effekt: ~4–8× Speichereffizienz vs. naive Allokation (Kwon et al., OSDI'23)
- **Code [Production Ready]:** `vllm serve` mit `--block-size 16` (Default), `--swap-space 4` (CPU Offload GB)

### 4.2 Continuous Batching (Iteration-Level Scheduling)
- Problem: Statisches Batching → Padding Waste, Head-of-Line Blocking
- Lösung: Iteration-Level Scheduling — fertige Sequenzen verlassen Batch, neue rutschen nach
- vLLM v0.6+: Unified Scheduler (V1 Architecture), kein separater Scheduler mehr
- **Tuning-Parameter [Production Ready]:**
  ```bash
  --max_num_seqs 32              # Max gleichzeitige Sequenzen (ehem. max-num-seqs)
  --max_num_batched_tokens 8192  # Token-Budget pro Iteration (neu v0.6+)
  --enable_chunked_prefill       # Lange Prefills chunken, Decode nicht blockieren
  ```
- **Trade-off:** Interactive (kleines Batch, TTFT-Prio) vs. Batch (großes Batch, Durchsatz-Prio)
- **Merke:** Batch-Size ist keine Konstante — sie schwankt pro Iteration. Monitoring: `num_running_seqs`, `num_waiting_seqs`

### 4.3 Prefix Caching (Automatisch in vLLM v0.6+)
- Mechanismus: Hash-basiert (System Prompt + User Prefix), LRU-Eviction
- Hit Rate Metrik: `prefix_cache_hit_rate` (Prometheus)
- **Multi-Tenant SaaS:** System Prompt pro Tenant cachen → 50%+ Prefill-Einsparung bei hohem Overlap
- **Code [Production Ready]:** `--enable_prefix_caching` (Default ON), `--cpu_offload_gb` für Cache auf CPU

### 4.4 Quantisierung: Formate & Methoden
| Format | Use Case | Kernel | Quality Risk |
|--------|----------|--------|--------------|
| AWQ-INT4 (awq_marlin) | GPU Inference, Standard | Marlin (vLLM Default) | Niedrig, Kalibrierung nötig |
| GPTQ | Legacy, CPU/GPU | Exllama / Marlin | Veraltet in vLLM, nicht empfohlen |
| GGUF (Q4_K_M) | CPU, Edge, llama.cpp | llama.cpp | Gering, aber langsamer auf GPU |
| FP8 (H100+) | Native H100, 2× Throughput | TensorRT-LLM / vLLM FP8 | Kalibrierung kritisch, ~1% Delta |
| FP4 (Blackwell) | Next-Gen, Preview | TRT-LLM | Noch experimentell |

**Qualitätsregression Methodik (NEU, obligatorisch):**
- Golden Dataset (Ch 9): 500 annotierte SupportPilot-Tickets (PII-scrubbed)
- Metriken: Klassifikation F1, Extraktion F1, Tone Accuracy
- Baseline: FP16 → Optimiert: AWQ-INT4/FP8
- Akzeptanz: Delta ≤ 2% F1 (Domain-spezifisch), keine Regression auf Safety-Subset
- **Anti-Pattern:** „INT4 reicht für 90%“ — ohne Messung ist das Glücksspiel

### 4.5 Speculative Decoding
- Mechanismus: Draft Model (klein) generiert k Token → Target Model verifiziert parallel
- Speedup = 1 / (1 - Acceptance Rate) bei idealer Parallelisierung
- **Acceptance Rate Threshold:** >60% (unterhalb: Overhead > Gewinn)
- **Draft Model Auswahl:** Shared Tokenizer Pflicht (Llama-3.2-1B für Llama-3.1-70B)
- **vLLM Config [Production Ready]:**
  ```bash
  --speculative_model meta-llama/Llama-3.2-1B-Instruct
  --num_speculative_tokens 5
  --speculative_max_model_len 2048
  ```
- **Advanced (Priority 2):** EAGLE (Token-Tree), Medusa (Multi-Head), Lookahead (kein Draft Model)
- **Monitoring:** `speculative_acceptance_rate` Alert <50%

---

## 5. Production Example: SupportPilot Self-Hosting Journey

**Narrative Arc (ersetzt E-Commerce RAG Autornotiz):**

### Ausgangslage (Baseline FP16)
- Hardware: 4×A100 80GB (NVLink), vLLM TP=4
- Modell: `meta-llama/Llama-3.1-70B-Instruct` (FP16)
- Config [Production Ready]:
  ```yaml
  # vllm-config.yaml
  model: meta-llama/Llama-3.1-70B-Instruct
  tensor_parallel_size: 4
  gpu_memory_utilization: 0.85
  max_num_seqs: 16
  enable_chunked_prefill: true
  enable_prefix_caching: true
  dtype: float16
  ```
- Ergebnisse: TTFT p95 2.1s, TPOT 68ms, Throughput 180 tok/s, GPU Util 45%, VRAM 140GB

### Schritt 1: AWQ-INT4 Quantisierung
- Kalibrierung: 512 SupportPilot-Tickets (repräsentativ, nicht zufällig)
- Tool: AutoAWQ → `--quantization awq_marlin`
- VRAM: 140GB → 38GB → passt auf 2×A100
- Quality Check: Golden Dataset (500 Tickets) — Delta -1.2% F1 (akzeptabel)
- Ergebnisse: TTFT p95 1.3s, TPOT 38ms, Throughput 320 tok/s, GPU Util 62%

### Schritt 2: Continuous Batching + Chunked Prefill
- Config: `--max_num_seqs 32 --max_num_batched_tokens 8192`
- Ergebnisse: TTFT p95 1.1s, Throughput 680 tok/s, GPU Util 78%
- **Trade-off beobachtet:** TTFT leicht schlechter bei Burst (Queueing), aber Durchsatz 2×

### Schritt 3: Speculative Decoding
- Draft: `meta-llama/Llama-3.2-1B-Instruct` (shared Tokenizer)
- Config: `--num_speculative_tokens 5`
- Acceptance Rate: 72% (gemessen über 10k Requests)
- Ergebnisse: TPOT 19ms, Throughput 1.100 tok/s, TTFT 1.2s (Draft-Overhead)
- **Merke:** SpecDec hilft TPOT, nicht TTFT. Für Chat (Interaktiv) wertvoll, für Batch weniger.

### Kostenvergleich (Evidence-Based)
| Setup | Hardware/Monat | API Äquivalent (GPT-4o) | Ersparnis |
|-------|----------------|------------------------|-----------|
| 4×A100 FP16 | ~$3.600 | $8.500 | 58% |
| 2×A100 AWQ-INT4 + Opt | ~$1.800 | $8.500 | 79% |

**Cross-Refs:**
- `\ref{chap:finetuning}` — LoRA für Domain-Adaptation (Ch 13)
- `\ref{chap:routing}` — Router entscheidet 3B vs 70B (Ch 18)
- `\ref{chap:guardrails}` — PII Detection, Halluzination Check (Ch 19)

---

## 6. Trade-offs

**Entscheidungsmatrix (Tabelle):**

| Optimierung | Gewinn | Kosten/Risiko | Wann Ja | Wann Nein |
|-------------|--------|---------------|---------|-----------|
| AWQ-INT4 | 3-4× VRAM, 2× Throughput | Kalibrierung nötig, -1-2% Quality | GPU Memory Limit, Quality Budget ≤2% | Kein Memory Druck, Quality Critical |
| FP8 (H100) | 2× Throughput vs FP16 | Kalibrierung sensibel, HW abhängig | H100/Blackwell, Max Throughput | A100/älter, keine Kalibrier-Daten |
| Continuous Batching | 2-5× Throughput | TTFT Varianz, Tuning Aufwand | Hohes Volumen, Batch-Toleranz | Strenge TTFT SLA (<500ms) |
| Speculative Decoding | 1.5-2.5× TPOT | Draft Model VRAM, Acceptance Rate Risk | Interactive Chat, Acceptance >60% | Batch Inference, Low Acceptance |
| Prefix Caching | Bis 50% Prefill weniger | Cache Memory, Eviction Policy | Multi-Tenant, System Prompts | Einmalige Prompts, kein Overlap |
| KV Offload (CPU/Disk) | Größere Contexts | Latency Spike bei Swap | Context > GPU voll | Latency Critical |
| TensorRT-LLM | 2-4× vLLM auf H100 | Engine Build, weniger flexibel | H100 Fleet, Max Perf | Schnelle Iteration, Custom Logic |

**Merke-Box:**
```latex
\merke{
Keine Optimierung ist kostenlos. Quantisierung kostet Quality. SpecDec kostet VRAM + Acceptance Risk. 
Continuous Batching kostet TTFT-Varianz. Entscheide basierend auf DEINEN SLAs — nicht Benchmarks.
}
```

**Cross-Ref:** Ch 17 (Production) für SLA-Definitionen, Ch 18 (Routing) für Modell-Auswahl.

---

## 7. Failure Modes

| Failure Mode | Symptom | Ursache | Detection | Mitigation |
|--------------|---------|---------|-----------|------------|
| **OOM bei Traffic Spike** | Worker Crash, 503 | `gpu_memory_utilization` zu hoch, Batch Spike | DCGM: `gpu_memory_used > 90%` | `--gpu_memory_utilization 0.85`, Autoscaling, Request Queue |
| **Draft Rejection Storm** | TPOT explodiert, Throughput ↓ | Acceptance Rate <50% (Domain Shift) | Prometheus: `speculative_acceptance_rate < 0.5` | Auto-Disable SpecDec, Alert, Draft Model Retrain |
| **KV Cache Fragmentation** | OOM trotz freiem VRAM, schwankende TPOT | Lange Sequenzen, keine PagedAttention | `vllm:gpu_cache_usage_perc > 95%` | PagedAttention (Default), `--block-size 16`, Prefix Caching |
| **Cold Start auf Scale-Up** | 60-120s bis Ready | Model Load + CUDA Init + JIT | Deployment Time Metric | Model Pinning (Triton), Pre-warm Dummy Requests, `--enforce_eager` |
| **Prefix Cache Thrashing** | Hit Rate <20%, Prefill nicht schneller | Zu viele verschiedene System Prompts | `prefix_cache_hit_rate < 0.2` | Tenant-Affinity Routing, Cache Size Limit |
| **Quantization Quality Drift** | F1 fällt nach Model Update | Neue Kalibrierung nicht repräsentativ | Golden Dataset CI Pipeline | Automatischer Quality Gate bei Deploy |
| **CUDA Graph Capture Fail** | Startup Crash, `CUDA error: invalid configuration` | Dynamic Shapes, zu große Batch | Startup Logs | `--enforce_eager` für Debug, feste `max_num_batched_tokens` |

**Praxishinweis-Box:**
```latex
\praxishinweis{
Failure Modes sind keine Theorie — sie passieren in der ersten Produktionswoche. 
Baue Alerts **bevor** du Optimierungen aktivierst. Ohne `speculative_acceptance_rate` Alert 
fliegst du blind bei SpecDec.
}
```

---

## 8. Evaluation

### 8.1 Benchmark Methodology (NEU, obligatorisch für jedes Zahl)
**Template für JEDE quantitative Behauptung:**
```
Metric: [TTFT / TPOT / Throughput / VRAM / Quality Delta / Cost]
Baseline: [FP16, no batching, vLLM v0.5, Llama-3.1-70B]
Optimized: [AWQ-INT4, Continuous Batching batch=32, SpecDec draft=Llama-3.2-1B]
Dataset: [ShareGPT / MT-Bench / Custom SupportPilot Tickets — n=500]
Hardware: [4×A100-80GB, NVLink, CUDA 12.4, Driver 550.x]
Software: [vLLM 0.6.3, FlashAttn 2.6, PyTorch 2.4]
Methodology: [Warmup=20, Runs=100, Seed=42, Report=P50/P95/P99]
Result: [TTFT P95: 1200ms → 850ms (-29%)]
Limitations: [Single-Node TP only; no PP; synthetic prompt distribution]
```

### 8.2 Golden Dataset Quality Regression (Cross-Ref Ch 9)
- 500 SupportPilot Tickets (PII-scrubbed), annotiert: Intent, Entities, Tone
- Metriken: Macro F1 (Klassifikation), Token F1 (Extraktion), Tone Accuracy
- CI Gate: `pytest --quality-gate` — Fail bei Delta >2% F1

### 8.3 Performance Benchmarks (Repräsentative Zahlen MIT Methodik)
| Config | TTFT P95 | TPOT P95 | Throughput | GPU Util | VRAM | Methodik Ref |
|--------|----------|----------|------------|----------|------|--------------|
| FP16, TP=4, Static | 2100ms | 68ms | 180 tok/s | 45% | 140GB | Bench v1.0 |
| AWQ-INT4, TP=2 | 1300ms | 38ms | 320 tok/s | 62% | 38GB | Bench v1.1 |
| + Cont. Batching (32) | 1100ms | 35ms | 680 tok/s | 78% | 42GB | Bench v1.2 |
| + SpecDec (5 tok, 72% AR) | 1200ms | 19ms | 1100 tok/s | 82% | 46GB | Bench v1.3 |

**Warnung:** Zahlen sind SupportPilot-spezifisch (Ticket-Länge, PII, Domain). Nicht blind übertragen.

### 8.4 Acceptance Rate Measurement (SpecDec)
- Messfenster: 10k Requests, sliding window 1h
- Metriken: Mean AR, P10 AR (Tail), Token-level vs Sequence-level
- Alert: P10 AR < 50% → Auto-Disable

---

## 9. Best Practices

1. **Starte mit Baseline, nicht mit Optimierung** — Messen vor Tunen
2. **Quantisierung IMMER mit Golden Dataset validieren** — Keine Ausnahmen
3. **Speculative Decoding nur bei AR >60% aktivieren** — Monitoring Pflicht
4. **Continuous Batching: `max_num_batched_tokens` vor `max_num_seqs` tunen** — Token-Budget ist der Hebel
5. **Prefix Caching: Tenant-Affinity im Load Balancer** — Cache Hit Rate maximieren
6. **GPU Memory Utilization 0.85-0.90** — Puffer für Spikes, Fragmentierung
7. **Model Pinning + Pre-warm für Autoscaling** — Cold Start <10s Ziel
8. **Benchmark CI: Nightly Runs mit festem Seed, Dataset, Hardware** — Regressionen fangen
9. **Dokumentiere Config als Code (YAML)** — Reproduzierbarkeit, GitOps
10. **Cost Model aktuell halten** — Hardware Preise ändern sich schneller als Modell Qualitäten

**Merke-Box:**
```latex
\merke{
Best Practice: „Es kommt drauf an“ ist keine Antwort. 
Antwort: „Für SupportPilot (PII, 100 req/min, <2s TTFT) ist AWQ-INT4 + Cont.Batching + SpecDec der Sweet Spot. 
Dein Sweet Spot findest du nur durch Messen.“
}
```

---

## 10. Anti-Patterns

| Anti-Pattern | Warum Schlecht | Besser |
|--------------|----------------|--------|
| **„INT4 reicht immer“** | Quality Regression unbemerkt, Domain Shift | Golden Dataset Gate, CI Pipeline |
| **SpecDec ohne Acceptance Monitoring** | Silent Degradation, Throughput Collapse | Alert <60% AR, Auto-Disable |
| **`gpu_memory_utilization 0.95`** | OOM bei minimaler Fragmentierung | 0.85-0.90, Headroom für Spikes |
| **Static Batching in Production** | 50%+ GPU Idle, Head-of-Line Blocking | Continuous Batching (Default vLLM) |
| **Benchmark ohne Warmup/Seed** | Nicht reproduzierbar, Marketing-Zahlen | Fixed Seed=42, Warmup=20, P50/P95/P99 |
| **Quantisierung ohne Kalibrier-Daten** | AWQ braucht repräsentative Daten | 512+ Domain-Samples, nicht Wikipedia |
| **Ein Model für alles (70B für Klassifikation)** | Overkill, teuer, langsam | Router (Ch 18): 3B für Simpel, 70B für Komplex |
| **Kein Prefix Caching bei Multi-Tenant** | 50%+ Prefill Waste | Tenant-Affinity + `--enable_prefix_caching` |
| **Cold Start ignorieren** | Scale-Up = 2min Downtime | Model Pinning, Pre-warm, Eager Mode |
| **Nur vLLM evaluieren** | TRT-LLM 2-4× schneller auf H100 | Hardware-abhängig evaluieren, nicht religös |

---

## 11. Production Checklist (NEU)

### Pre-Deploy
- [ ] Baseline Benchmark dokumentiert (Methodik Template)
- [ ] Golden Dataset Quality Gate in CI integriert
- [ ] Quantisierung kalibriert mit Domain-Daten (n≥512)
- [ ] SpecDec Acceptance Rate >60% auf Holdout-Set validiert
- [ ] Continuous Batching Parameter getunt (`max_num_batched_tokens`)
- [ ] Prefix Caching Hit Rate >40% bei Staging-Traffic
- [ ] GPU Memory Utilization ≤0.85 gesetzt
- [ ] Model Pinning / Pre-warm Script bereit
- [ ] Prometheus Alerts: `gpu_memory_used>90%`, `speculative_acceptance_rate<0.5`, `prefix_cache_hit_rate<0.2`

### Deploy
- [ ] Config als YAML versioniert (GitOps)
- [ ] Docker Image: vLLM 0.6.3 + FlashAttn 2.6 + CUDA 12.4 pinned
- [ ] Rolling Deploy: Max 1 Worker gleichzeitig, Health Check `/health`
- [ ] Canary: 5% Traffic, Golden Dataset Smoke Test

### Post-Deploy (Day 1-7)
- [ ] TTFT P95 < Target (SupportPilot: 2s)
- [ ] TPOT P95 < Target (SupportPilot: 50ms)
- [ ] GPU Util 70-85% (Interactive) / >85% (Batch)
- [ ] Acceptance Rate >60% (SpecDec)
- [ ] Prefix Cache Hit Rate >40%
- [ ] Quality Gate: Golden Dataset F1 Delta ≤2%
- [ ] Cost Tracking: $/1k Tokens vs. API Baseline

### Ongoing
- [ ] Nightly Benchmark Regression Test
- [ ] Monthly Quantisierung Re-Kalibrierung (neue Tickets)
- [ ] Quarterly Hardware Cost vs. API Re-Evaluation
- [ ] vLLM Version Upgrade: Changelog prüfen, Staging validieren

---

## 12. Exercises

### Übung 1: Baseline Messen (Didactic)
- Setup: vLLM + Llama-3.2-1B auf 1×A100 (oder Colab T4)
- Task: `benchmark_throughput.py` mit ShareGPT Dataset (n=100)
- Messen: TTFT P50/P95, TPOT P50/P95, Throughput, GPU Util
- Deliverable: Markdown Report mit Methodik Template

### Übung 2: Quantisierung + Quality Gate (Production Ready)
- AWQ-INT4 für Llama-3.2-3B mit AutoAWQ kalibrieren (512 Samples)
- Golden Dataset: 200 annotierte Samples (Intent Klassifikation)
- CI Pipeline: `pytest --quality-gate` fail bei >2% F1 Delta
- Deliverable: PR mit Config, Benchmark Vorher/Nachher, Quality Report

### Übung 3: Speculative Decoding Tuning (Production Ready)
- Draft: Llama-3.2-1B, Target: Llama-3.1-8B (shared Tokenizer)
- Sweep: `num_speculative_tokens` [3, 5, 7, 10]
- Messen: Acceptance Rate, TPOT, TTFT, Throughput
- Decision: Welcher Wert für Interactive Chat? Für Batch?
- Deliverable: Entscheidung mit Daten, Alert-Regel für AR<60%

### Übung 4: Continuous Batching vs Static (Didactic)
- Synthetischer Load: 50 parallele Requests, gemischte Länge (100-2000 Token)
- Config A: Static Batching (vLLM `--disable_chunked_prefill`)
- Config B: Continuous Batching (Default v0.6+)
- Vergleichen: Throughput, TTFT Verteilung, GPU Util
- Deliverable: Plot + 3-Satz Fazit

### Übung 5: Cold Start Messung (Production Ready)
- Container Start → First Token Latency messen (100 Runs)
- Varianten: Cold, Pre-warmed (Dummy Request), Model Pinned (Triton)
- Deliverable: Tabelle + Empfehlung für Autoscaling Policy

---

## 13. Further Reading

### Primary Sources (Implementations)
- **vLLM v0.6+ Docs:** https://docs.vllm.ai — V1 Architecture, Chunked Prefill, Prefix Caching Default
- **TensorRT-LLM:** https://github.com/NVIDIA/TensorRT-LLM — FP8, In-Flight Batching, Pipeline Parallelism
- **Triton Inference Server:** https://github.com/triton-inference-server/server — Model Repository, Ensembles, BLS
- **AutoAWQ / Marlin:** https://github.com/mit-han-lab/llm-awq — `--quantization awq_marlin`
- **EAGLE Speculative Decoding:** https://github.com/SafeAILab/EAGLE — Token-Tree SpecDec
- **llama.cpp Server:** https://github.com/ggml-org/llama.cpp/tree/master/examples/server — GGUF HTTP Server

### Benchmarks & Methodology
- **vLLM Benchmarks:** https://github.com/vllm-project/vllm/tree/main/benchmarks — Reproducible Scripts
- **DCGM Exporter:** https://github.com/NVIDIA/dcgm-exporter — GPU Metrics für Prometheus
- **MLPerf Inference:** https://mlcommons.org/benchmarks/inference/ — Standardisierte Benchmarks

### Papers (Theory)
- Kwon et al., *"PagedAttention: Efficient Memory Management for LLM Serving"* (OSDI'23) — PagedAttention Grundlagen
- Leviathan et al., *"Fast Inference from Transformers via Speculative Decoding"* (ICML'23) — SpecDec Theorie
- Chen et al., *"Speculative Decoding with Big Little Decoder"* (ICLR'24) — EAGLE/Medusa
- Sheng et al., *"High-Throughput Generative Inference with Continuous Batching"* (vLLM Blog) — Continuous Batching

### Cross-Chapter References
- `\ref{chap:caching}` — Prompt Caching, Semantic Cache (Ch 10)
- `\ref{chap:evaluation}` — Golden Dataset, Quality Gates (Ch 9)
- `\ref{chap:finetuning}` — Multi-LoRA Serving, LoRA Training (Ch 13)
- `\ref{chap:routing}` — Model Router, Cost-Aware Routing (Ch 18)
- `\ref{chap:guardrails}` — PII Detection, Halluzination Guard (Ch 19)
- `\ref{chap:production}` — K8s Deployment, Autoscaling, Observability (Ch 17)
- `\ref{chap:ai_engineer_rolle}` — Cost Awareness, AI Engineer Role (Ch 1)

---

## Outline Metadata

**Status:** A+ Outline Complete — Ready for Chapter Writer  
**Research Report:** `research/11_inferenz_optimierung-a-plus-research.md`  
**Target Chapter File:** `chapters/11_inferenz_optimierung.tex`  
**Estimated Length:** 35-45 Seiten (inkl. Code, Tabellen, Diagramme)  
**Review Gates:**
1. Outline Review (this doc) ✓
2. Chapter Writer Draft → Writing Editor → Final Polish
3. LaTeX Compile Check (`latexmk -xelatex -outdir=_build main.tex`)
4. Cross-Ref Verification (keine `??`)
5. German Spellcheck (de-DE + en-US)

**Key Decisions Documented:**
- SupportPilot Self-Host Narrative ersetzt E-Commerce RAG Story
- Skip Box für API-Nutzer
- Alle Zahlen an Evidence Template gebunden
- TensorRT-LLM + Triton als eigene Sections
- Benchmark Methodik als eigenes Section
- Code Labels: [Production Ready] / [Didactic Example]
- Model Names: Llama-3.1-70B / Llama-3.2-1B (kein 3.3)
- vLLM v0.6+ Flags (underscores, defaults)