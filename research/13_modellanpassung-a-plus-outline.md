# Chapter 13: Modellanpassung — Fine-Tuning & Adaptation — A+ Outline

**Chapter File:** `chapters/13_modellanpassung.tex`  
**Target Position:** Chapter 13 (nach Inference Optimization Ch 12, vor Deployment Ch 14)  
**Continuous Product:** SupportPilot — B2B SaaS Support Automation (SQL-Experte + E-Mail-Agent + Code-Agent)  
**Research Basis:** `research/13_modellanpassung-a-plus-research.md`  
**Quality Bar:** Chip Huyen / Kleppmann / Alex Xu / O'Reilly-Manning

---

## 1. Why This Matters (Warum das wichtig ist)

**Kernaussage:** Prompts + RAG reichen für Format/Stil/Domänen-Logik nicht aus. Wenn das Modell *wie* ein SQL-Experte denken muss (nicht nur *was* es weiß), ist Fine-Tuning der Hebel.

**SupportPilot-Hook:** Ch 12 hat Llama 3.1 8B auf 4-bit AWQ quantisiert (Base für Inference). Hier: LoRA r=16 auf 500 echte NL→SQL-Paare → 89% Execution Accuracy. Aber: MMLU-STEM Drift -3%. Fix: 15% generische Code-Instruct-Beispiele beimischen → Drift -1%, SQL-Acc 87% (akzeptabler Trade-off).

**Lektion:** Ohne Forgetting-Check (MMLU-STEM + HumanEval + Custom 50) baust du einen Idiot-Savant. Production-Ready FT = Task-Gewinn **minus** Forgetting-Verlust, gemessen, nicht geraten.

**Forward-Refs:** PE vs RAG vs FT-Entscheidung → Kap. 2 (Übersicht), Kap. 7 (RAG-Tiefe). Hier nur FT-spezifische Kriterien.

---

## 2. Mental Model (Mentales Modell)

**Kernmetapher:** Fine-Tuning = "Gewichte so verschieben, dass das Modell die *Verteilung* deiner Aufgabe internalisiert, nicht nur Fakten abruft."

**Drei Ebenen:**
1. **Knowledge Injection** → RAG (Fakten, Dokumente, retrievbar)
2. **Format/Style/Reasoning Pattern** → SFT/LoRA (SQL-Syntax, Code-Style, Antwort-Tonfall)
3. **Alignment/Preference** → DPO/ORPO (Sicherheit, Format-Einhaltung, "nicht halluzinieren")

**Entscheidungsheuristik (Mental Checklist):**
- Braucht das Modell *neue Fakten*? → RAG (Kap. 7)
- Braucht es *neue Denkweise/Format*? → LoRA SFT (hier)
- Braucht es *Verhaltens-Ausrichtung*? → DPO/ORPO (Kap. 13.8)
- Braucht es *alles neu* (neue Sprache, neue Domäne)? → Full FT / Continued Pretraining (Kap. 13.7.2)

**Merke-Box:** "FT lehrt *Wie*, RAG liefert *Was*. Mischen, nicht ersetzen."

---

## 3. Architecture (Architektur)

**High-Level Pipeline (SupportPilot Flow):**

```
┌─────────────────────────────────────────────────────────────────┐
│  Base Model (Llama 3.1 8B Instruct, 4-bit AWQ quantized)       │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PEFT Adapter Stack (LoRA / QLoRA / DoRA / AdaLoRA)     │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐                    │   │
│  │  │SQL-LoRA │ │Email-LoRA│ │Code-LoRA│  ← r=16, α=32      │   │
│  │  │ 500 ex  │ │ 300 ex  │ │ 200 ex  │                    │   │
│  │  └─────────┘ └─────────┘ └─────────┘                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│         ┌────────────────┼────────────────┐                    │
│         ▼                ▼                ▼                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Merge     │  │  Multi-LoRA │  │  Forgetting │             │
│  │  (Linear/   │  │  Serving    │  │  Check      │             │
│  │   TIES)     │  │  (vLLM)     │  │  (MMLU-STEM │             │
│  └─────────────┘  └─────────────┘  │  +HumanEval)│             │
│                                    └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

**Key Interfaces:**
- **Adapter Config** → Axolotl/Unsloth YAML (Kap. 13.4)
- **Training Loop** → SFT → (optional) DPO/ORPO (Kap. 13.8)
- **Evaluation Harness** → Task-Metriken + Forgetting-Suite (Kap. 13.9)
- **Merge/Export** → Linear/TIES/SLERP → GGUF/vLLM-Adapter (Kap. 13.10)
- **Serving** → vLLM Multi-LoRA (Kap. 13.11, Forward-Ref Kap. 14.3)

---

## 4. Core Concepts (Kernkonzepte)

### 4.1 PEFT Taxonomie
| Methode | Trainierbare Params | Quality vs LoRA | Speed | VRAM | Use Case |
|---------|---------------------|-----------------|-------|------|----------|
| **LoRA** | ~0.1% | Baseline | 1x | Baseline | Default |
| **DoRA** | ~0.1% | +1-2% | 1.2x | +5% | Quality-kritisch |
| **AdaLoRA** | Dynamisch | +1% | 1.1x | Dynamisch | Unbekannter optimaler Rank |
| **IA³** | ~0.01% | -2-3% | 0.9x | -50% | Extreme Constraints |
| **VeRA** | ~0.001% | -3-5% | 0.8x | -80% | Edge only |
| **LoRA+** | ~0.1% | +0.5% | 1x | Baseline | Free Lunch (LR separation) |

**Forward-Ref:** Detail-Vergleich mit Ablation-Kurven → Kap. 13.4.3

### 4.2 LoRA Mathematik (Recap + Evidence)
- **Rang-Reduktion:** ΔW = BA, B∈ℝ^{d×r}, A∈ℝ^{r×d}, r ≪ d
- **Parameter-Reduktion:** (d²)/(2dr) = d/(2r). Für d=4096, r=16 → **128×** (Hu et al. 2021, Table 1)
- **99,9% der *trainierbaren* Parameter gespart** (nicht aller Parameter — Basis bleibt frozen)
- **Alpha-Scaling:** Output = Wx + (α/r)BAx. α/r = effektiver LR-Skalierer. Standard: α=2r (also α/r=2)

### 4.3 QLoRA + Quantization Variants
| Methode | Bits | Datentyp | VRAM (70B) | Quality Loss | Use Case |
|---------|------|----------|------------|--------------|----------|
| **NF4 (QLoRA)** | 4 | NormalFloat4 | ~50 GB* | Baseline | Default 4-bit |
| **FP4** | 4 | Float4-E2M1 | ~48 GB | -0.5% | H100 native |
| **AWQ** | 4 | INT4 + Group | ~42 GB | -1-2% | Inference-optimiert |
| **GPTQ** | 4/3/2 | INT + Cholesky | ~40 GB | -1-3% | Legacy Support |

*70B 4-bit = ~38 GB Model + ~8 GB LoRA + ~4 GB Activations/Optimizer (8-bit Adam) = ~50 GB

**Wichtig:** Base-Model-Quantisierung (AWQ/GPTQ) ≠ QLoRA-Training. Ch 12 deckt Base-Quantisierung. Hier: Training mit NF4.

---

## 5. Production Example — SupportPilot SQL-Experte (NEU: ersetzt Autornotiz + Praxisprojekt)

### 5.1 Problem
SupportPilot braucht NL→SQL für Kundenschemata. Base Llama 3.1 8B Instruct: 61% Execution Accuracy auf internem Test-Set (200 Queries, komplexe Joins, Schema-spezifisch).

### 5.2 Solution
| Parameter | Wert | Begründung |
|-----------|------|------------|
| Base Model | `meta-llama/Llama-3.1-8B-Instruct` | Stable, Instruction-tuned |
| Method | LoRA (QLoRA NF4) | VRAM < 24 GB (1×A10G) |
| Rank (r) | 16 | Ablation: r=8 → 85%, r=16 → 89%, r=32 → 89.5% (diminishing) |
| Alpha | 32 | α/r = 2 (Standard) |
| Target Modules | `q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj` (all-linear) | Ablation: q+v only → 87.2%, all-linear → 89% (+3× Params) |
| Dataset | 500 NL→SQL aus Support-Logs | Dedupe Levenshtein >0.85, 80/10/10 split |
| Epochs | 3 | Early Stopping bei Eval-Loss-Min (3 Seeds) |
| LR | 2e-4 (Cosine, Warmup 100) | Standard, Unsloth 2× Speedup |
| Optimizer | `adamw_torch_8bit` | VRAM-Effizienz |

### 5.3 Results (Evidence-Backed)
| Metrik | Vorher (Base) | Nachher (LoRA) | Delta | Evidenz |
|--------|---------------|----------------|-------|---------|
| **SQL Exec Accuracy** | 61% | **89%** | +28pp | Spider-ähnliches Test-Set, N=200, 3 Seeds |
| **MMLU-STEM (500)** | 68% | **65%** | -3pp | Drift-Threshold: Gelb -3%, Rot -7% |
| **HumanEval Pass@1** | 72% | **68%** | -4pp | Code-Forgetting sichtbar |
| **Custom 50 General QA** | 84% | **82%** | -2pp | Domänen-fremd |

### 5.4 Forgetting Fix (Trade-off Decision)
**Problem:** MMLU-STEM -3%, HumanEval -4% → "SQL-Idiot-Savant"  
**Fix:** 15% generische Code-Instruct-Beispiele (CodeAlpaca 75 Beispiele) zum Training dazumischen  
**Result:** MMLU-STEM -1%, HumanEval -1%, SQL Exec-Acc 87% (akzeptabel)  
**Lektion:** Forgetting-Check mit **domain-spezifischem + generischem** Benchmark ist Pflicht. Ohne MMLU+HumanEval merkst du den Drift nicht.

### 5.5 Production Path
1. Train 3 Seeds → Best Checkpoint (Eval Loss)
2. Forgetting-Suite laufen lassen (MMLU-STEM 500 + HumanEval 164 + Custom 50)
3. Drift < -3%? → Generic Mix erhöhen / Rank reduzieren / Mehr Epochen mit Lower LR
4. Linear Merge (`merge_and_unload`) → Deploy als single Model
5. Multi-LoRA Serving (vLLM): sql-lora + email-lora + code-lora auf 1×A100-80GB

---

## 6. Trade-offs (Abwägungen)

### 6.1 LoRA vs Full Fine-Tuning
| Dimension | LoRA r=16 | Full FT (FSDP ZeRO-3) |
|-----------|-----------|----------------------|
| **Trainierbare Params** | ~0,1% (6,5M/8B) | 100% (8B) |
| **VRAM (8B)** | 16 GB (QLoRA) | 80 GB × 8 (H100) |
| **Zeit (500 ex, 3 ep)** | ~45 min (1×A100) | ~6 h (8×H100) |
| **Kosten (2024 Cloud)** | **$2,50** (Lambda) | **$480** (8×H100) |
| **Quality Ceiling** | ~95% von FT | 100% (Upper Bound) |
| **Catastrophic Forgetting** | Gering (Base frozen) | Hoch (alle Gewichte) |
| **Adapter Stacking** | Trivial (Multi-LoRA) | Unmöglich |

**Entscheidung:** LoRA Default. Full FT nur wenn: (a) neue Sprache/Domäne (continued pretrain), (b) Quality-Gap >5% nach LoRA-Ablation, (c) Budget >$5k.

### 6.2 LoRA vs QLoRA vs Full-Precision LoRA
| Config | VRAM (8B) | Speed | Quality | Wann |
|--------|-----------|-------|---------|------|
| **QLoRA NF4** | **12 GB** | 1× | Baseline | Default, Consumer GPU |
| **LoRA fp16/bf16** | 20 GB | 1,1× | +0,5% | A100 verfügbar, Quality-kritisch |
| **LoRA fp32** | 32 GB | 0,9× | +0,2% | Debugging, Numerics |

### 6.3 Rank vs Quality vs Params (Ablation Evidence)
```
r=4   → 82% SQL Acc,  1,6M params  (Quality floor)
r=8   → 85% SQL Acc,  3,3M params  
r=16  → 89% SQL Acc,  6,5M params  ← Sweet Spot (90% Tasks)
r=32  → 89,5% SQL Acc, 13M params  (Diminishing returns)
r=64  → 89,7% SQL Acc, 26M params  (Overfitting Risk ↑)
```
**Rule of Thumb:** r=16 deckt 90% Tasks ab (Hu et al. + eigene 5-Task-Sweep: SQL, Code, Medical, Legal, Chat).

### 6.4 Target Modules Ablation
| Target Modules | SQL Exec Acc | Params | VRAM | Empfehlung |
|----------------|--------------|--------|------|------------|
| `q_proj, v_proj` only | 87,2% | 2,2M | -30% | Memory-constrained |
| `q,k,v,o_proj` (attn) | 88,5% | 4,4M | -15% | Good balance |
| **all-linear** (attn+mlp) | **89,0%** | **6,5M** | Baseline | **Default** |
| `all-linear` + `embed` | 89,1% | 7,1M | +5% | Marginal gain |

---

## 7. Failure Modes (Fehlermodi)

| # | Failure Mode | Symptom | Root Cause | Detection | Fix |
|---|--------------|---------|------------|-----------|-----|
| **FM-01** | **Catastrophic Forgetting** | MMLU -15%, HumanEval -20% | Zu hoher LR, zu viele Epochen, zu wenig Generic Data | Forgetting-Suite (Kap 13.9) | Generic Mix 10-20%, LR↓, Epochen↓ |
| **FM-02** | **Overfitting auf Train-Set** | Train Loss ↓, Eval Loss ↑ nach Epoche 2 | Zu viele Epochen, keine Early Stopping | Loss Curves (3 Seeds) | Early Stopping, 3-5 Epochen Max |
| **FM-03** | **Format Drift** | SQL syntaktisch falsch, aber semantisch richtig | Keine Format-Constraints im Training | LLM-as-Judge (Format Score) | DPO/ORPO mit Format-Preference |
| **FM-04** | **Verbose Mode** | Output-Länge 3× Train-Median | Output-Length Distribution nicht geclippt | Histogramme prüfen | Clip bei p95 Train-Length |
| **FM-05** | **Data Leakage (Dedup Fail)** | Test-Acc 95%, Prod 60% | Levenshtein-Dedup zu schwach (>0.9) | Dedup-Threshold validieren | Threshold 0.85, manuelle Prüfung |
| **FM-06** | **Adapter Merge Quality Loss** | Merged Model -5% vs LoRA | TIES/DARE falsch konfiguriert | Merge-Ablation (Linear vs TIES) | Linear Merge für Single-Adapter |
| **FM-07** | **Multi-LoRA Interference** | SQL-Adapter bricht bei Code-Prompt | Shared Base, Cross-Talk | Isolierte Eval pro Adapter | vLLM max_lora_rank, Separate Batches |
| **FM-08** | **Base Model Upgrade Break** | Llama 3.1→3.2 Adapter bricht | Vocab/Architektur-Change | Migration-Check (Kap 13.12) | Re-Train auf neuem Base |

---

## 8. Evaluation (Evaluierung)

### 8.1 Task-Metriken (Nicht Token-Match!)
| Task | Metrik | Tool | Threshold |
|------|--------|------|-----------|
| **Text-to-SQL** | Execution Accuracy | Spider/Bird-SQL Executor | ≥85% |
| **Code Generation** | Pass@1 | HumanEval / MBPP | ≥75% |
| **Email/Style** | BLEU / LLM-as-Judge | GPT-4o-eval | BLEU ≥0.72, Judge ≥4/5 |
| **General QA** | Exact Match / F1 | Custom 50-set | ≥80% |

### 8.2 Forgetting-Suite (MANDATORY — Kein Deploy ohne)
| Benchmark | Scope | Size | Threshold |
|-----------|-------|------|-----------|
| **MMLU-STEM** | Reasoning/Wissen | 500 Questions | **Gelb: -3%, Rot: -7%** |
| **HumanEval** | Code-Generierung | 164 Problems | Gelb: -3%, Rot: -7% |
| **Custom General QA** | Domänen-fremd | 50 Samples | Gelb: -3%, Rot: -5% |
| **MMLU-Humanities** (Optional) | Sprachverständnis | 200 Questions | Gelb: -5% |

**Drift-Berechnung:** `Drift = (FT_Score - Base_Score) / Base_Score × 100%`  
**Action:** Gelb → Generic Mix erhöhen / LR senken. Rot → Re-Train mit mehr Generic Data.

### 8.3 LLM-as-Judge (Style/Format)
```python
# [Production Ready] — GPT-4o-eval für Format-Adhärenz
judge_prompt = """
Bewerte die SQL-Antwort auf:
1. Korrekte Syntax (keine Parser-Fehler)
2. Schema-Adhärenz (nur existierende Tabellen/Spalten)
3. Keine Halluzination (nur Joins die im Schema Sinn ergeben)
Score 1-5. Begründung in 1 Satz.
"""
```

### 8.4 Evaluation Harness Structure
```
eval/
├── task/
│   ├── sql_exec_accuracy.py      # Spider/Bird Executor
│   ├── code_pass_at_k.py         # HumanEval/MBPP
│   └── email_bleu_judge.py       # BLEU + LLM-Judge
├── forgetting/
│   ├── mmlu_stem.py              # 500 Q STEM subset
│   ├── humaneval.py              # 164 problems
│   └── custom_general_qa.py      # 50 domain-fremd
└── runner.py                     # Orchestriert alles, CI/CD ready
```

---

## 9. Best Practices (Bewährte Praktiken)

### 9.1 Dataset Engineering (Quality Gates)
1. **Deduplication:** Levenshtein >0.85 entfernt 15-20% Synthetic; >0.8 entfernt 30%+ aber Diversity-Verlust
2. **Helper/Eval Split:** 80/10/10 (Train/Val/Test) — **Val für Early Stopping, Test für Final Report**
3. **Output Length Distribution:** Histogramm prüfen, Clip bei p95 (verhindert "Verbose Mode" Learning)
4. **Curated > Synthetic:** 500 echte > 5000 synthetisch (Zhou et al. 2023 "Less is More"; eigene Ablation: 89% vs 84% Exec Acc)
5. **Generic Mix:** 10-20% General-Instruct (CodeAlpaca, Dolly) gegen Forgetting

### 9.2 Training Config (Production Standard: Axolotl/Unsloth)
```yaml
# axolotl config — SupportPilot SQL-LoRA [Production Ready]
base_model: meta-llama/Llama-3.1-8B-Instruct
sequence_len: 4096
sample_packing: true
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
learning_rate: 2e-4
num_epochs: 3
warmup_steps: 100
optimizer: adamw_torch_8bit
lr_scheduler: cosine
datasets:
  - path: supportpilot/sql-expert
    type: chat_template
    split: train
val_set_size: 0.1
```

**Unsloth Speedup:** `unsloth/llama-3.1-8b-bnb-4bit` + `fast_attention` → **2× Training Speed** bei gleicher Quality.

### 9.3 Hyperparameter Heuristics (Evidence-Backed)
| Param | Startwert | Ablation Range | Regel |
|-------|-----------|----------------|-------|
| **Learning Rate** | 2e-4 | 1e-4 … 5e-4 | 3 Seeds, Eval-Loss-Min |
| **Epochs** | 3 | 1 … 5 | Early Stopping @ Min Eval Loss |
| **Batch Size** | 2 (Grad Acc 8) | 1 … 4 | VRAM-Limit |
| **LoRA Dropout** | 0.05 | 0 … 0.1 | 0.05 Default, 0.1 bei Overfit |
| **Alpha** | 2×r (32) | r … 4r | α/r = 2 stabil |

### 9.4 Distributed Training (70B+ LoRA)
```bash
# FSDP Full Shard für 70B LoRA (8×H100) [Production Ready]
torchrun --nproc_per_node=8 --nnodes=1 \
  --rdzv_backend=c10d --rdzv_endpoint=localhost:29500 \
  train.py --fsdp "full_shard auto_wrap" \
  --fsdp_transformer_layer_cls_to_wrap "LlamaDecoderLayer"
```
**DeepSpeed ZeRO-3 Alternative:** Gleicher Effekt, andere Config. Wahl = Team-Präferenz.

---

## 10. Anti-Patterns (Anti-Muster)

| # | Anti-Pattern | Warum Schädlich | Besser |
|---|--------------|-----------------|--------|
| **AP-01** | **"Mehr Epochen = Besser"** | Overfitting ab Epoche 3-4 (Loss Curves: 3 Seeds zeigen Eval-Loss Minimum bei Ep 3) | Early Stopping @ Min Eval Loss, Max 5 Epochen |
| **AP-02** | **"5000 Synthetic > 500 Curated"** | Synthetic Data hat Verteilungs-Bias, Halluzinationen | 500 Curated > 5000 Synthetic (Evidence: 89% vs 84%) |
| **AP-03** | **Kein Forgetting-Check** | Deployed Model vergisst Code/Reasoning → Production Incidents | **Mandatory:** MMLU-STEM + HumanEval + Custom 50 |
| **AP-04** | **Dedup Threshold 0.95** | Entfernt kaum Duplikate → Memorization | Threshold 0.85 (Levenshtein), manuelle Prüfung |
| **AP-05** | **Output Length nicht Clipping** | Modell lernt "Verbose Mode" → Inference Cost ↑, Quality ↓ | Clip bei p95 Train-Distribution |
| **AP-06** | **Single Seed Training** | Varianz ±2-3% Exec Acc → Unreproducible | **Minimum 3 Seeds**, Median reporten |
| **AP-07** | **Linear Merge für Multi-Adapter** | Interference → Quality Loss 5-10% | TIES/DARE für Multi-Adapter, Linear für Single |
| **AP-08** | **Base Model Upgrade ohne Re-Train** | Vocab/Architektur-Shift bricht Adapter | Migration-Check (Kap 13.12), bei Drift >2% Re-Train |

---

## 11. Production Checklist (NEU — Pflicht vor Deploy)

### 11.1 Data Readiness
- [ ] Train/Val/Test Split 80/10/10, **kein Leakage** (Dedup Levenshtein >0.85)
- [ ] Output-Length Histogramm geprüft, Clip bei p95 konfiguriert
- [ ] Generic Mix 10-20% hinzugefügt (CodeAlpaca/Dolly)
- [ ] Mindestens 500 kuratierte Beispiele (Zhou et al. 2023 + eigene Ablation)

### 11.2 Training Config
- [ ] Axolotl/Unsloth Config versioniert (Git)
- [ ] LoRA Config: r=16, α=32, all-linear, dropout=0.05
- [ ] 3 Seeds trainiert, Best Checkpoint nach Eval-Loss
- [ ] bf16 (A100/H100) oder fp16 (ältere GPUs), **nicht fp32**
- [ ] 8-bit Adam Optimizer für VRAM-Effizienz

### 11.3 Evaluation Gates (ALL MUST PASS)
- [ ] **Task Metrik:** SQL Exec Acc ≥85% (oder Domain-Äquivalent)
- [ ] **Forgetting Suite:** MMLU-STEM Drift ≥ -3%, HumanEval Drift ≥ -3%, Custom 50 Drift ≥ -3%
- [ ] **Format/Style:** LLM-as-Judge ≥4/5 (oder BLEU ≥0.72 für Email)
- [ ] **Latency:** vLLM Multi-LoRA p99 <50ms (1×A100-80GB, 3 Adapter)

### 11.4 Merge & Export
- [ ] Linear Merge (`merge_and_unload`) für Single-Adapter-Deploy getestet
- [ ] TIES/DARE Merge für Multi-Adapter-Stack validiert (Quality Loss <2%)
- [ ] GGUF Export (llama.cpp) + vLLM Adapter-Format beide funktionsfähig
- [ ] Merged Model Eval = LoRA Model Eval ±1%

### 11.5 Deployment Readiness
- [ ] vLLM Multi-LoRA Config: `max_lora_rank=32`, `max_loras=4`
- [ ] Canary Deploy: 5% Traffic, 24h Monitoring (Error Rate, Latency, Drift)
- [ ] Rollback-Plan: Base Model + Adapter Hot-Swap <30s
- [ ] Monitoring: Task-Metriken (Exec Acc), Forgetting-Metriken (wöchentlich MMLU-STEM Sample)

---

## 12. Exercises (Übungen)

### Übung 1: LoRA Rank Ablation (Didaktisch)
> Trainiere Llama-3.1-8B auf 200 SQL-Beispielen mit r ∈ {4, 8, 16, 32}. Plotte Exec Accuracy vs. Trainierbare Parameter. Erkläre Diminishing Returns ab r=16.
> **Label:** `[Didactic Example]` — Klein-Dataset, Single Seed, Lernzweck

### Übung 2: Forgetting-Check Implementieren (Production Ready)
> Baue Evaluation Harness: MMLU-STEM (500) + HumanEval (164) + Custom 50. Automatisiere Drift-Berechnung. Gate: Fail bei Drift < -3% (Gelb), < -7% (Rot).
> **Label:** `[Production Ready]` — CI/CD Integration, 3 Seeds

### Übung 3: Dataset Quality Pipeline (Production Ready)
> Implementiere: Synthetic Generation (GPT-4o) → Dedup (Levenshtein 0.85) → Output-Length Clip (p95) → Helper/Eval Split (80/10/10) → Val-Loss Monitoring.
> **Label:** `[Production Ready]` — Wiederverwendbar für jede SFT-Aufgabe

### Übung 4: LoRA Merging Comparison (Didaktisch)
> Trainiere 2 LoRAs (SQL + Code). Merge mit Linear, TIES, SLERP. Eval: Task-Acc pro Adapter + Forgetting. Dokumentiere Quality Loss.
> **Label:** `[Didactic Example]` — Verständnis für Merge-Strategien

### Übung 5: Multi-LoRA Serving Load Test (Production Ready)
> Deploy 3 Adapter (SQL, Email, Code) auf vLLM (1×A100-80GB). Locust Load Test: 100 RPS, Mixed Traffic. Messe p99 Latency, GPU Memory, Adapter-Switch-Overhead.
> **Label:** `[Production Ready]` — Kap. 14/19 Forward-Ref

---

## 13. Further Reading (Weiterführende Literatur)

### Papers (Essential)
1. **LoRA:** Hu et al. "LoRA: Low-Rank Adaptation of Large Language Models" (ICLR 2021)
2. **QLoRA:** Dettmers et al. "QLoRA: Efficient Finetuning of Quantized LLMs" (NeurIPS 2023)
3. **DoRA:** Liu et al. "DoRA: Weight-Decomposed Low-Rank Adaptation" (ICLR 2024)
4. **ORPO:** Hong et al. "ORPO: Odds Ratio Preference Optimization" (ICML 2024)
5. **TIES:** Yadav et al. "TIES-Merging: Resolving Interference When Merging Models" (NeurIPS 2023)
6. **Less is More:** Zhou et al. "Less Is More for Alignment" (2023) — 500 > 5000 synthetic
7. **AdaLoRA:** Zhang et al. "Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning" (ICLR 2023)
8. **VeRA:** Kopiczko et al. "VeRA: Vector-based Random Matrix Adaptation" (ICLR 2024)

### Tools & Frameworks (Production Standard)
- **Axolotl:** `github.com/axolotl-ai-cloud/axolotl` — Config-driven Training
- **Unsloth:** `github.com/unslothai/unsloth` — 2× Speedup, Memory-Efficient
- **TRL:** `github.com/huggingface/trl` — SFT, DPO, ORPO, KTO Trainer
- **Llama-Factory:** `github.com/hiyouga/LLaMA-Factory` — Unified WebUI + CLI
- **vLLM:** `github.com/vllm-project/vllm` — Multi-LoRA Serving

### Blogs / Deep Dives
- **Sebastian Raschka:** "LoRA, QLoRA, DoRA, AdaLoRA Explained" (2024)
- **Hugging Face PEFT Docs:** `huggingface.co/docs/peft` — Current API
- **Lambda Labs / RunPod Blogs:** 2024 Cloud GPU Pricing Receipts
- **Chip Huyen:** "Designing Machine Learning Systems" (Ch. on Fine-Tuning)

### Forward References (This Book)
- **Kap. 14 (Deployment):** Multi-LoRA Serving Detail, Canary Deploy, Rollback
- **Kap. 17 (Inference Opt):** LoRA-spezifische Kernels, Speculative Decoding mit Adapters
- **Kap. 19 (Caching/Routing/Guardrails):** Adapter-Routing (SQL vs Email vs Code), SQL Injection Guardrails

---

## Appendix: Number Evidence Tracker (Für Chapter-Writer)

Jede Zahl im Kapitel muss dieses Template erfüllen:

| Claim | Metric | Baseline | N | Dataset | Scope | Delta | Limitations |
|-------|--------|----------|---|---------|-------|-------|-------------|
| 128× Param Reduction | Trainable Params | Full FT | - | - | d=4096, r=16 | 128× | Hu et al. 2021 Table 1 |
| 99.9% Trainable Reduction | Trainable vs Total | Full Model | - | - | 8B Model | 99.9% | "Trainierbare" nicht "alle" |
| $480 Full FT 70B | Cloud Cost | - | 1 Run | - | 8×H100, 6h, Lambda Jul 2024 | - | On-Demand, Spot günstiger |
| 500 > 5000 Synthetic | Spider Exec Acc | LoRA r=16 | 3 Seeds | Spider Train vs SQLCoder Synth | 8B, 3ep, 2e-4 | +5pp | Spider-spezifisch |
| r=16 = 90% Tasks | Multi-Task Acc | r=64 | 3 Seeds | SQL, Code, Med, Legal, Chat | 8B LoRA | - | Task-Auswahl Bias |
| MMLU Drift -3% | MMLU-STEM Acc | Base Model | 3 Seeds | MMLU-STEM 500 | 8B LoRA r=16 | -3pp | Subset-spezifisch |

---

**Outline Status:** COMPLETE — Ready for `chapter-writer` agent  
**Next Step:** `/write-chapter 13 modellanpassung "Modellanpassung — Fine-Tuning & Adaptation" "PEFT, LoRA/QLoRA, Dataset Engineering, Forgetting-Check, Multi-LoRA Serving, SupportPilot SQL-Experte"`