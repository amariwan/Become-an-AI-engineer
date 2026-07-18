# Outline: Chapter 09 — Evaluation und Metriken (Target: Kap. 6)

## 1. Why this matters
- Evaluation ist die **einzige** Engineering-Disziplin, die probabilistische Systeme deterministisch beherrschbar macht
- Ohne Golden Set + CI-Gate = Blindflug bei jedem Prompt-Change
- Chip Huyen: "Evaluation first" — nicht nachgeschoben, sondern **vor** RAG, Agents, FT
- SupportPilot: Ohne Eval wusste das Team nicht, ob Prompt-v3 besser oder schlechter war — erst Golden Set (100 Cases) + Multi-Judge + CI-Gate machte Regressions in 2 Min sichtbar (statt 2 Wochen durch User-Beschwerden)

## 2. Mental Model
- **Drei Dimensionen, ein Trade-off-Dreieck**: Quality ↔ Cost ↔ Latency
- LLM ≠ deterministische Funktion → Testing ≠ klassisches Unit-Testing
- **Offline** (Golden Set vor Deploy) + **Online** (Tracing + Drift + A/B in Prod) — keine ersetzt die andere
- **Proxy vs. Business Metrik**: Faithfulness korreliert nicht automatisch mit Customer Satisfaction
- Evaluation ist **kontinuierlicher Prozess**, kein einmaliges Artefakt

## 3. Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                           │
│  Lint → Golden Dataset → Multi-Judge → Cost/Latency Gate   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Production Monitoring                       │
│  Tracing (Langfuse) → Metrics (P95, Cost, Faithfulness)    │
│       → Alerting (Drift, Cost Spike, Quality Drop)          │
│       → Dashboard (Grafana/Langfuse) → A/B Test Framework   │
└─────────────────────────────────────────────────────────────┘
```
Komponenten:
1. **Golden Dataset** (versioniert, wachsend, Git-getaggt)
2. **Evaluation Runner** (parallel, cached, budget-gated)
3. **LLM Judge** (Multi-Judge: 3 Modelle, Majority Vote, Agreement-Metrik)
4. **Tracing Layer** (Prompt-Hash, Tokens, Latency, Cost, Validation-Status)
5. **Dashboard + Alerting** (Quality < 0.7, Cost/Query > €0.02, P95 > 2s)

## 4. Core Concepts
### 4.1 Golden Dataset — Fundament
- Struktur: Input + Expected Output (Keywords / JSON Schema / Reference Answer)
- 50–100 Cases Start → wächst mit jedem Prod-Fehler
- Versionierung: `golden_v1.json` → `golden_v2.json` + Git Tag `eval/golden-v2`
- Synthetische Generierung nur als **Seed**, 20% manuell geprüft

### 4.2 LLM-as-a-Judge — Bias Taxonomy & Mitigation
| Bias | Manifestation | Mitigation |
|------|---------------|------------|
| Verbosity | GPT-4o bevorzugt lange Antworten | Rubric: "Kürze = Bonus", Length-Normalisierung |
| Self-Preference | Modell bewertet eigenen Stil höher | **Multi-Judge**: 3 verschiedene Modell-Familien |
| Position Bias | Erste Antwort in Pairwise gewinnt | **Position Swapping**: beide Reihenfolgen testen |
| Style Bias | Claude = vorsichtig, Gemini = strukturiert | Rubric-basiert statt freier Skala |
| Calibration Drift | Judge wird im Laufe der Zeit "nachsichtiger" | Monatliche Human-Calibration (Krippendorff α ≥ 0.8) |

**Multi-Judge Implementation**: 3 Modelle (verschiedene Familien) → Majority Vote + Agreement-Score (konsens ≥ 66% = valide)

### 4.3 RAG-spezifische Metriken (für Kap. 7 Forward-Ref)
- **Hit Rate @ K**: Relevantes Chunk in Top-K? (Binary)
- **MRR @ K**: Rang des ersten relevanten Chunks
- **Faithfulness**: % der Answer-Tokens durch Retrieved Chunks belegt (RAGAS-Style)
- **Answer Relevance**: Beantwortet die Answer die *eigentliche* Query?
- **Context Precision**: Signal/Rauschen im übergebenen Kontext

### 4.4 Drift Detection — Algorithmen
- **KS-Test** (Kolmogorov-Smirnov): Embedding-Distribution Shift (p < 0.01 → Alert)
- **PSI** (Population Stability Index): Token-Länge, Kosten/Query, Latency-Percentile
- **Embedding Shift**: Mean-Cosine-Distanz zu Referenz-Batch > Threshold
- **Quality Drift**: Faithfulness/Relevance über 7-Tage-Fenster linearer Trend < -5%

### 4.5 Human Evaluation Protocol
- **Annotation Guidelines**: 3-seitiges PDF mit Beispielen (Good/Bad/Edge)
- **Krippendorff's α**: Inter-Annotator-Agreement Ziel ≥ 0.8
- **Sample Size**: Min 50 Cases/Week, stratifiziert nach Query-Type
- **Blind**: Annotatoren sehen nicht, welcher Prompt/Model dahintersteckt

## 5. Production Example — SupportPilot Evaluation Journey
**Ausgangslage**: Prompt-v1 deployed, "fühlt sich gut an", aber keine Metriken.

**Schritt 1 — Golden Set Aufbau (Woche 1)**:
- 80 reale User-Queries aus Logs gesampelt (stratifiziert: 30% Status, 25% Rechnung, 20% Kündigung, 15% Technisch, 10% OOD)
- Manuelle Annotation: Expected Keywords + JSON Schema + "Should Not Contain"
- Baseline: Prompt-v1 → Pass Rate 72%, Avg Faithfulness 0.61, Cost/Query €0.018, P95 1.8s

**Schritt 2 — CI-Gate etabliert (Woche 2)**:
- GitHub Action: `pytest eval/golden.py --threshold 0.85`
- Multi-Judge (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro) → Majority Vote
- Budget Gate: Max $5/Run, Cache 80% Savings

**Schritt 3 — Regression gefangen (Woche 3)**:
- Prompt-v2 (neue Few-Shot Examples) → CI: Pass Rate 78% (grün), aber Faithfulness 0.58 (rot)
- Auto-Rollback verhindert Deploy
- Root Cause: Neues Example halluzinierte "30 Tage Rückgabe" statt "14 Tage"

**Schritt 4 — Production Drift erkannt (Monat 2)**:
- Langfuse Alert: Faithfulness Trend -8% über 14 Tage
- Ursache: Provider hob gpt-4o-mini stillschweigend auf neue Version (2024-07-18)
- Fix: Model Pinning `gpt-4o-mini-2024-07-18` + Canary 5% Traffic

**Ergebnis nach 3 Monaten**:
- Pass Rate: 72% → 94% (Golden Set)
- Halluzinationsrate: 8% → 1.2% (Faithfulness + Auto-Retry)
- Cost/Query: €0.018 → €0.012 (-34% durch Token-Budget-Check in CI)
- Regressions-Erkennung: 2 Min statt 2 Wochen

**Messrahmen für obige Zahlen**:
- Baseline: Prompt-v1, n=80 Golden Cases, 3 Judge-Modelle, Agreement ≥ 66%
- Evaluation Method: Offline Golden Set + Online 10% Sample Human Review
- Dataset: SupportPilot Production Queries Jan–Mar 2024, stratified
- n: 80 (Golden) + 200/woche (Online Sample)
- Metric: Pass Rate (Binary), Faithfulness (0-1), Cost/Query (EUR), P95 Latency (ms)
- What Changed: Golden Set + CI Gate + Multi-Judge + Model Pinning + Drift Alerts
- Limitations: Kein A/B Test (Traffic zu niedrig), Human Review nur 10%, Judge-Kalibrierung monatlich

## 6. Trade-offs
| Entscheidung | Option A | Option B | Empfehlung |
|--------------|----------|----------|------------|
| Judge-Count | Single (billig) | Multi-Judge 3x (teuer) | **Multi-Judge** für CI-Gate; Single für Exploration |
| Metric Type | Proxy (Faithfulness) | Business (CSAT) | **Beide**: Proxy im CI, Business im Monthly Review |
| Dataset Size | 50 (schnell) | 500+ (robust) | **Start 50**, wöchentlich +5 aus Prod-Fehlern |
| Human Eval | Wöchentlich 50 | Monatlich 200 | **Wöchentlich 50** stratifiziert; α ≥ 0.8 prüfen |
| Drift Sensitivity | KS-Test (sensitiv) | PSI (robust) | **KS für Embeddings**, PSI für Kosten/Latency |
| A/B Test | Full Randomisierung | Canary (5%) | **Canary für Prompt-Changes**, Full A/B für Model Swaps |

## 7. Failure Modes
| Failure Mode | Symptom | Detection | Prevention |
|--------------|---------|-----------|------------|
| **Judge Bias nicht kalibriert** | Judge-Score ↑, Human-Score ↓ | Monthly Krippendorff α < 0.8 | Monatliche Human-Calibration |
| **Golden Set veraltet** | Pass Rate ↑, Prod-Quality ↓ | Online/Offline Gap > 10% | Jeder Prod-Fehler → Golden Set + CI Fail |
| **Dataset Leakage** | Perfekt auf Golden, Müll in Prod | Train/Test Split verwechselt | Streng getrennte Splits, Versionierung |
| **Metric Gaming** | Optimierung auf Faithfulness → Answer Relevance ↓ | Guardrail-Metriken im Dashboard | **Immer** Primär + Sekundär + Guardrail |
| **Cost Explosion in Eval** | $50/Run statt $5 | Budget Gate in CI | Max $5/Run, Cache 80%, Delta-Eval |
| **Alert Fatigue** | Drift-Alerts täglich, keiner schaut | Alert/Week > 3 ohne Action | SLO-basiert: nur Alert bei SLO-Verletzung |

## 8. Evaluation — Meta-Evaluation (Wie evaluiere ich meine Evaluation?)
- **Offline/Online Correlation**: Pearson r zwischen Golden-Set-Pass-Rate und Prod-Quality (Ziel: r > 0.7)
- **Judge Calibration**: Monthly Human vs. Judge Agreement (Krippendorff α)
- **False Positive Rate**: Alerts fired / True Regressions (Ziel: < 30%)
- **Time to Detect**: Median Zeit von Regressions-Einführung bis Alert (Ziel: < 10 Min)
- **Cost per Detection**: Eval-Kosten / gefundene Regression (Ziel: < $10)

## 9. Best Practices
1. **Golden Dataset versionieren** — Git Tags `eval/golden-v{N}`, Changelog pro Version
2. **CI-Gate hart** — Exit Code 1 bei Pass Rate < 85% ODER Faithfulness < 0.8 ODER Cost > Budget
3. **Multi-Judge Pflicht** — 3 Modelle, verschiedene Familien, Majority Vote + Agreement
4. **Budget Gate in CI** — Max $5/Run, Delta-Eval für geänderte Prompts
5. **Prompt-Hash in Traces** — Jeder Trace verknüpft Prompt-Version → Golden-Set-Run
6. **Synthetisch → Human Pipeline** — LLM generiert Test-Cases → Human validiert → Golden Set
7. **Drift Detection Dual** — KS-Test (Embeddings) + PSI (Cost/Latency) + Quality Trend
8. **Human Evaluation Protocol** — Guidelines, Krippendorff α ≥ 0.8, Blind, Stratified
9. **A/B Test Framework** — Canary 5%, Minimum Detectable Effect definiert, Power Analysis
10. **Documentation** — Jeder Metrik: Definition, Baseline, Threshold, Owner, Last Reviewed

## 10. Anti-Patterns
1. **Evaluation ohne Golden Dataset** → LLM-Judge misst nur Judge-Meinung
2. **Judge = zu evaluierendes Modell** → Selbstbestätigung, keine externe Validierung
3. **Nur Accuracy messen** → System 100% Accuracy, aber 10s Latency / $1/Query / unsicher
4. **Einmaliges Dataset** → Nach 3 Monaten irrelevant (User-Verhalten, Model-Updates, Produkt)
5. **Human Evaluation ignorieren** → LLM-Judge ersetzt keine Domänen-Expertise (Medizin, Recht, Finance)
6. **Online Monitoring vergessen** → Offline grün, Prod rot (Model Drift, Data Drift, Provider Drift)
7. **Single Metric Optimization** → Faithfulness ↑ aber Answer Relevance ↓ = nutzlose Antworten
8. **Kein Budget Gate** → $500 Eval-Run blockiert CI, Team deaktiviert Tests

## 11. Production Checklist
- [ ] Golden Dataset ≥ 50 Cases, versioniert in Git, wächst wöchentlich
- [ ] CI Pipeline: Lint → Golden Set → Multi-Judge → Cost/Latency Gate → Exit Code
- [ ] Multi-Judge: 3 Modelle (verschiedene Familien), Agreement ≥ 66%
- [ ] Tracing: Jeder Call geloggt (Prompt-Hash, Tokens, Latency, Cost, Validation)
- [ ] Dashboard: Quality (Faithfulness/Relevance), Cost/Query, P95 Latency, Error Rate
- [ ] Alerts: Quality < 0.7, Cost > 2x Baseline, P95 > 2s, Drift (KS/PSI) p < 0.01
- [ ] Model Pinning: Explizite Versionen (`gpt-4o-mini-2024-07-18`), Canary 5%
- [ ] Human Eval: Wöchentlich 50 Cases, Krippendorff α ≥ 0.8, Guidelines dokumentiert
- [ ] A/B Framework: Canary für Prompts, Full Randomisierung für Model Swaps
- [ ] Runbooks: Quality Drop, Cost Spike, Provider Outage, Drift Alert

## 12. Exercises
1. **Golden Set Bootstrap**: Erstelle 30 Cases für SupportPilot (10 Status, 8 Rechnung, 7 Kündigung, 5 Technisch) mit Expected Keywords + JSON Schema
2. **Multi-Judge Implementation**: Implementiere Majority Vote + Agreement für 3 Judge-Modelle
3. **CI Gate**: GitHub Action mit Pass Rate ≥ 85%, Faithfulness ≥ 0.8, Cost ≤ $5
4. **Drift Alert**: KS-Test auf Embedding-Distribution + PSI auf Cost/Query, Alert bei p < 0.01
5. **Human Evaluation**: Annotation Guidelines für 3 Annotatoren, Krippendorff α Berechnung
6. **A/B Test Design**: Sample Size Calculator für Prompt-v1 vs v2 (MDE 5%, Power 80%, α 5%)
7. **Cost Anomaly Detection**: Rolling 7-Day Cost/Query, Alert bei +50% vs. Baseline

## 13. Further Reading
- **Primary**: Chip Huyen — "AI Engineering", Kap. 3 (Evaluation); "Designing ML Systems", Kap. 8
- **Papers**: 
  - Liu et al. (2023) — "LLM-as-a-Judge" (Bias Taxonomy)
  - Sarti et al. (2024) — "RAGAS: Automated Evaluation of RAG"
  - Yan et al. (2024) — "Corrective RAG" (CRAG Quality Gate)
  - Zheng et al. (2024) — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
- **Tools**: Langfuse (Open Source), DeepEval, Promptfoo, RAGAS, OpenAI Evals, Garak (Security)
- **Standards**: ISO/IEC 25059 (AI Quality Model), NIST AI RMF (Evaluation)