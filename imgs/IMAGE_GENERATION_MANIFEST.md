# Image Generation Manifest für gemini-create-photo

## Ordner-Struktur
```
images/
├── 01_rolle/
├── 02_modelle/
├── 03_landschaft/
├── 04_openai_api/
├── 05_token/
├── 06_prompt/
├── 07_rag/
├── 08_agents/
├── 09_eval/
├── 10_deployment/
├── 11_inference_opt/
├── 12_caching/
├── 13_finetuning/
├── 14_multimodal/
├── 15_mlops/
├── 16_security/
└── appendix/
```

---

## KAPITEL 07: RAG (07_rag_vector_datenbanken.tex)

### FIG 1: RAG Pipeline Overview
**Target:** Nach Zeile 62 (Architektur-Block)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/07_rag/fig01_rag_pipeline_overview.pdf}`

```json
{
  "prompt": "Technical diagram: RAG system architecture with two parallel pipelines. LEFT: Offline Indexing Pipeline - Documents (PDF, DB, HTML icons) -> Loader -> Chunker (scissors icon) -> Embedder (vector icon) -> Vector DB (cylinder icon). RIGHT: Online Runtime Pipeline - User Query -> Embedder -> Vector DB (ANN search arrow) -> Re-Ranker (optional, diamond) -> Context Builder -> LLM -> Structured Output. Clean minimalist style, dark blue/teal color scheme, arrows showing data flow, German labels.",
  "file": "images/07_rag/fig01_rag_pipeline_overview.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 62,
    "latex_width": "0.9\\textwidth",
    "caption": "RAG-System: Offline Indexing Pipeline (links) und Online Runtime Pipeline (rechts)",
    "label": "fig:rag-pipeline-overview"
  }
}
```

### FIG 2: Chunking Strategies Comparison
**Target:** Nach Zeile 309 (Recursive Chunking Abschnitt)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/07_rag/fig02_chunking_strategies.pdf}`

```json
{
  "prompt": "Technical illustration: Four chunking strategies side by side. 1) Fixed-Size: Rectangle divided into equal blocks, red warning at boundaries. 2) Recursive: Hierarchical splitting - paragraphs -> sentences -> words, green checkmarks. 3) Markdown/Header: Document with heading hierarchy preserved as metadata tags. 4) Code: Python code split at function/class boundaries. Minimalist technical style, blue/green/red color coding for good/bad/neutral.",
  "file": "images/07_rag/fig02_chunking_strategies.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 309,
    "latex_width": "0.85\\textwidth",
    "caption": "Chunking-Strategien im Vergleich: Fixed-Size vs Recursive vs Markdown vs Code-spezifisch",
    "label": "fig:chunking-strategies"
  }
}
```

### FIG 3: Hybrid Search Architecture
**Target:** Nach Zeile 467 (pgvector Hybrid Search Code)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/07_rag/fig03_hybrid_search.pdf}`

```json
{
  "prompt": "Architecture diagram: Hybrid Search flow. Query splits into two paths: TOP PATH - Vector Search: Query -> Embedding -> HNSW Index (graph visualization) -> Cosine Similarity Scores. BOTTOM PATH - BM25 Search: Query -> Tokenization -> Inverted Index -> BM25 Scores. MERGE: Weighted Combination (0.7 * Vector + 0.3 * BM25) -> Reranked Results. PostgreSQL/pgvector branding, technical diagram style.",
  "file": "images/07_rag/fig03_hybrid_search.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 467,
    "latex_width": "0.9\\textwidth",
    "caption": "Hybrid Search: Vector Similarity (HNSW) + BM25 kombiniert in pgvector",
    "label": "fig:hybrid-search"
  }
}
```

### FIG 4: Advanced RAG Techniques
**Target:** Nach Zeile 530 (Re-Ranker Code Block)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/07_rag/fig04_advanced_rag_techniques.pdf}`

```json
{
  "prompt": "Four-panel technical diagram showing advanced RAG techniques: 1) HyDE: User Query -> LLM generates Hypothetical Document -> Embed -> Search. 2) Multi-Query: Query -> LLM generates 3-5 variants -> Parallel Search -> Deduplicate -> Top-K. 3) Cross-Encoder Re-Ranker: Query+Doc pairs -> Joint Attention -> Relevance Scores -> Re-ranked Top-5. 4) CRAG: Retrieval -> Evaluator (LLM Judge) -> Score 1-5 -> Generate/Refuse/Web Search. Clean grid layout, arrows, minimal text.",
  "file": "images/07_rag/fig04_advanced_rag_techniques.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 530,
    "latex_width": "0.9\\textwidth",
    "caption": "Fortgeschrittene RAG-Techniken: HyDE, Multi-Query, Cross-Encoder Re-Ranker, CRAG",
    "label": "fig:advanced-rag"
  }
}
```

### FIG 5: RAG Evaluation Metrics
**Target:** Nach Zeile 613 (Metrics Table)
**LaTeX:** `\includegraphics[width=0.8\textwidth]{images/07_rag/fig05_evaluation_metrics.pdf}`

```json
{
  "prompt": "Visual explanation of RAG evaluation metrics. Four metric cards: 1) Hit Rate @ K: Binary relevance in top-K (green check/red X). 2) MRR: Rank of first relevant result (1/rank formula). 3) NDCG @ K: Position-weighted relevance (discounted cumulative gain). 4) Faithfulness: Answer claims vs. Retrieved evidence (citation overlap). Technical infographic style, formulas shown, German labels.",
  "file": "images/07_rag/fig05_evaluation_metrics.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 613,
    "latex_width": "0.8\\textwidth",
    "caption": "RAG-Evaluationsmetriken: Hit Rate, MRR, NDCG, Faithfulness",
    "label": "fig:rag-metrics"
  }
}
```

### FIG 6: RAG Security Layers
**Target:** Nach Zeile 826 (Security Code Block)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/07_rag/fig06_security_layers.pdf}`

```json
{
  "prompt": "Security architecture diagram: Three defense layers for RAG. LAYER 1 (Input): Document Upload -> Security Scanner (regex patterns) -> Block/Allow -> Indexing. LAYER 2 (Storage): PostgreSQL with Row Level Security (RLS) policy visualization - Tenant A sees only Tenant A data. LAYER 3 (Output): LLM Response -> Output Filter (forbidden patterns) -> Safe Response / Blocked. Shield icons, red/green indicators, technical style.",
  "file": "images/07_rag/fig06_security_layers.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 826,
    "latex_width": "0.9\\textwidth",
    "caption": "RAG-Sicherheit: Drei Verteidigungsebenen - Input Scanning, Tenant Isolation (RLS), Output Filter",
    "label": "fig:rag-security"
  }
}
```

### FIG 7: Latency Breakdown
**Target:** Nach Zeile 742 (Latency Table)
**LaTeX:** `\includegraphics[width=0.8\textwidth]{images/07_rag/fig07_latency_breakdown.pdf}`

```json
{
  "prompt": "Horizontal stacked bar chart showing RAG query latency breakdown. Segments: Query Embedding (50-200ms, blue), Hybrid Search (30-80ms, teal), Re-Ranking (40-100ms, orange), Context Building (<1ms, gray), LLM Generation (500-1500ms, dark blue - largest segment). Total p50: 700-1200ms, Total p99: 1500-2500ms. Annotations in German, clean data viz style.",
  "file": "images/07_rag/fig07_latency_breakdown.png",
  "metadata": {
    "chapter": "07_rag_vector_datenbanken",
    "insert_after_line": 742,
    "latex_width": "0.8\\textwidth",
    "caption": "Latenz-Budget einer RAG-Query -- LLM Generation dominiert",
    "label": "fig:rag-latency"
  }
}
```

---

## KAPITEL 08: AI AGENTEN (08_ai_agenten.tex)

### FIG 1: Agent Loop Architecture
**Target:** Nach Zeile 252 (Agent Loop Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/08_agents/fig01_agent_loop.pdf}`

```json
{
  "prompt": "Circular flow diagram: AI Agent Loop with 4 phases. OBSERVE (eye icon) -> PLAN (brain/lightbulb) -> ACT (tool/gear icon) -> REFLECT (checkmark/magnifying glass) -> back to OBSERVE. Center: 'LLM as Reasoning Engine'. Arrows show flow, 'Goal not reached?' decision diamond between Reflect and Observe. Minimalist, dark theme, German labels.",
  "file": "images/08_agents/fig01_agent_loop.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 252,
    "latex_width": "0.9\\textwidth",
    "caption": "Der fundamentale Agent-Loop: Observe → Plan → Act → Reflect",
    "label": "fig:agent-loop"
  }
}
```

### FIG 2: Agent Components Architecture
**Target:** Nach Zeile 288 (Agent Components Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/08_agents/fig02_agent_components.pdf}`

```json
{
  "prompt": "Box architecture diagram: AI Agent container with 6 internal components in 2 rows. ROW 1: LLM (GPT-4o/Claude), Memory (History + Vector), Tool Registry (search, calc, db_query icons). ROW 2: Planner (Strategy), Executor (Tool Run), Safety Guard (HITL, Budget). Clean box-in-box layout, connection lines, technical documentation style.",
  "file": "images/08_agents/fig02_agent_components.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 288,
    "latex_width": "0.9\\textwidth",
    "caption": "Agenten-Komponenten: LLM, Memory, Tool Registry, Planner, Executor, Safety Guard",
    "label": "fig:agent-components"
  }
}
```

### FIG 3: AgentOS Architecture
**Target:** Nach Zeile 324 (AgentOS Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/08_agents/fig03_agentos_architecture.pdf}`

```json
{
  "prompt": "Layered architecture diagram: AgentOS as platform. TOP: Agent Runtime (LLM, Memory, Tool Calls). MIDDLE: Policy Engine (Permissions, Safety Rules), Observability (Logging, Metrics, Alerts). BOTTOM: Workflow Orchestrator, Tool Sandbox (Connections, Secrets, APIs), State Storage (Memory, Cache, Audit Logs). Horizontal layers, vertical integration lines, enterprise software architecture style.",
  "file": "images/08_agents/fig03_agentos_architecture.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 324,
    "latex_width": "0.9\\textwidth",
    "caption": "AgentOS-Architektur: Runtime, Policy Engine, Observability, Orchestrierung, Sandbox, State Storage",
    "label": "fig:agentos-arch"
  }
}
```

### FIG 4: Single vs Multi-Agent Comparison
**Target:** Nach Zeile 399 (Comparison Table)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/08_agents/fig04_single_vs_multi_agent.pdf}`

```json
{
  "prompt": "Split comparison diagram. LEFT: Single Agent - One LLM center, 5 tools around it, simple loop arrow. RIGHT: Multi-Agent - Supervisor (crown icon) connecting to 4 Worker Agents (Research, Analysis, Writing, Review) each with own tools. Arrows show delegation and aggregation. Labels: Complexity, Planning, Fault Tolerance, Cost, Latency. Technical comparison infographic.",
  "file": "images/08_agents/fig04_single_vs_multi_agent.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 399,
    "latex_width": "0.9\\textwidth",
    "caption": "Single-Agent vs. Multi-Agent: Architektur, Komplexität, Kosten, Latenz",
    "label": "fig:single-vs-multi"
  }
}
```

### FIG 5: ReAct Pattern Flow
**Target:** Nach Zeile 625 (ReAct Code)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/08_agents/fig05_react_pattern.pdf}`

```json
{
  "prompt": "Sequence diagram: ReAct Agent execution flow. User Query -> LLM (Thought) -> Tool Call (Action) -> Tool Result (Observation) -> LLM (Thought) -> Tool Call -> Tool Result -> ... -> Final Answer. Numbered steps 1-6. Speech bubbles for LLM thoughts, box for tool execution, clean UML sequence diagram style.",
  "file": "images/08_agents/fig05_react_pattern.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 625,
    "latex_width": "0.85\\textwidth",
    "caption": "ReAct Pattern: Thought → Action → Observation Loop",
    "label": "fig:react-pattern"
  }
}
```

### FIG 6: Plan-and-Solve Pattern
**Target:** Nach Zeile 657 (Plan-and-Solve Code)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/08_agents/fig06_plan_and_solve.pdf}`

```json
{
  "prompt": "Two-phase diagram: PHASE 1 (Planning): Task -> LLM Planner -> Structured Plan [Step 1, Step 2, Step 3...]. PHASE 2 (Execution): For each step -> Execute -> Result -> Accumulate. PHASE 3 (Synthesis): All Results -> LLM Synthesizer -> Final Answer. Dashed line between phases, clear separation.",
  "file": "images/08_agents/fig06_plan_and_solve.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 657,
    "latex_width": "0.85\\textwidth",
    "caption": "Plan-and-Solve: Planungsphase → Ausführungsphase → Synthese",
    "label": "fig:plan-and-solve"
  }
}
```

### FIG 7: Multi-Agent Patterns
**Target:** Nach Zeile 801 (Architecture Patterns Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/08_agents/fig07_multi_agent_patterns.pdf}`

```json
{
  "prompt": "Three-panel diagram showing Multi-Agent patterns: 1) SUPERVISOR-WORKER: User -> Supervisor -> [Worker A, Worker B, Worker C] parallel -> Supervisor aggregates -> Answer. 2) PIPELINE: User -> Agent A (Extract) -> Agent B (Analyze) -> Agent C (Generate) -> Answer. 3) DEBATE: Agent Pro + Agent Con -> Mediator -> Synthesis. Clean layout, distinct colors per pattern.",
  "file": "images/08_agents/fig07_multi_agent_patterns.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 801,
    "latex_width": "0.9\\textwidth",
    "caption": "Multi-Agent-Architekturmuster: Supervisor-Worker, Pipeline, Debate/Reflection",
    "label": "fig:multi-agent-patterns"
  }
}
```

### FIG 8: LangGraph State Machine
**Target:** Nach Zeile 720 (LangGraph Code)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/08_agents/fig08_langgraph_state_machine.pdf}`

```json
{
  "prompt": "State machine diagram for LangGraph workflow. Nodes: SUPERVISOR (diamond decision), RESEARCHER (rectangle), ANALYST (rectangle), WRITER (rectangle), END (circle). Edges: Supervisor -> Researcher (condition: research), Supervisor -> END (condition: end), Researcher -> Analyst, Analyst -> Writer, Writer -> END. Graph visualization, nodes with icons, directed edges with labels.",
  "file": "images/08_agents/fig08_langgraph_state_machine.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 720,
    "latex_width": "0.85\\textwidth",
    "caption": "LangGraph State Machine: Supervisor → Researcher → Analyst → Writer → END",
    "label": "fig:langgraph-statemachine"
  }
}
```

### FIG 9: Agent Security Guard
**Target:** Nach Zeile 1051 (Safety Guard Code)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/08_agents/fig09_security_guard.pdf}`

```json
{
  "prompt": "Security flow diagram: Agent Safety Guard pipeline. BEFORE TOOL: Step Counter (max_steps check) -> Tool Blacklist (shell, delete, email blocked) -> Domain Whitelist (internal APIs only) -> Allow/Deny. AFTER TOOL: Result -> Injection Scanner (patterns) -> Size Limiter (10k chars) -> Safe Output. Shield icons, red blocked paths, green allowed paths.",
  "file": "images/08_agents/fig09_security_guard.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 1051,
    "latex_width": "0.85\\textwidth",
    "caption": "Agent-Sicherheits-Guard: Pre-Tool Checks (Steps, Blacklist, Whitelist) + Post-Tool Filtering",
    "label": "fig:agent-security"
  }
}
```

### FIG 10: HITL Pattern
**Target:** Nach Zeile 1101 (HITL Code)
**LaTeX:** `\includegraphics[width=0.8\textwidth]{images/08_agents/fig10_hitl_pattern.pdf}`

```json
{
  "prompt": "Human-in-the-Loop workflow: Agent requests approval (action + context) -> Notification sent (Slack/Email/Teams icons) -> Human reviews -> Approve/Reject -> Agent continues/waits. Timeout path (300s) -> Auto-reject. State machine: PENDING -> APPROVED/REJECTED/TIMEOUT. Clean workflow diagram.",
  "file": "images/08_agents/fig10_hitl_pattern.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 1101,
    "latex_width": "0.8\\textwidth",
    "caption": "Human-in-the-Loop: Approval Request → Notification → Human Decision → Continue/Abort",
    "label": "fig:hitl-pattern"
  }
}
```

### FIG 11: Agent Latency Breakdown
**Target:** Nach Zeile 979 (Latency Table)
**LaTeX:** `\includegraphics[width=0.8\textwidth]{images/08_agents/fig11_agent_latency.pdf}`

```json
{
  "prompt": "Stacked horizontal bar chart: Agent Step Latency. LLM Planning (300-800ms), Tool Execution (50-500ms), Result Processing (100-300ms), Next Planning (300-800ms). Total per step: ~1-2s. Annotations: 'LLM calls dominate', 'Parallel tool calling saves 30-50%'. German labels, technical style.",
  "file": "images/08_agents/fig11_agent_latency.png",
  "metadata": {
    "chapter": "08_ai_agenten",
    "insert_after_line": 979,
    "latex_width": "0.8\\textwidth",
    "caption": "Latenz und Kosten pro Agent-Schritt (GPT-4o)",
    "label": "fig:agent-latency"
  }
}
```

---

## KAPITEL 11: INFERENCE OPTIMIZATION (11_inferenz_optimierung.tex)

### FIG 1: Prefill vs Decode Phases
**Target:** Nach Zeile 53 (Prefill/Decode Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/11_inference_opt/fig01_prefill_decode.pdf}`

```json
{
  "prompt": "Two-panel technical diagram. LEFT (Prefill - Parallel): Input tokens [T1][T2][T3]...[TN] all feeding into parallel matrix multiplication -> Single KV-Cache output -> Token N+1. RIGHT (Decode - Sequential): Token N+1 -> KV-Cache -> Token N+2 -> KV-Cache -> Token N+3... Memory bandwidth bottleneck icon on decode side. Compute icon on prefill side. German labels.",
  "file": "images/11_inference_opt/fig01_prefill_decode.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 53,
    "latex_width": "0.9\\textwidth",
    "caption": "LLM-Inference: Prefill-Phase (parallel, compute-bound) vs. Decode-Phase (sequentiell, memory-bound)",
    "label": "fig:prefill-decode"
  }
}
```

### FIG 2: Five Bottlenecks
**Target:** Nach Zeile 72 (Bottlenecks Table)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/11_inference_opt/fig02_five_bottlenecks.pdf}`

```json
{
  "prompt": "Five-card infographic: LLM Inference Bottlenecks. 1) VRAM: Model weights + KV-Cache overflow GPU -> Fix: Quantization, Multi-GPU. 2) Memory Bandwidth: Decode is memory-bound -> Fix: PagedAttention, Speculative Decoding. 3) Compute: Prefill needs matmul -> Fix: Tensor Parallelism, Flash Attention. 4) TTFT Latency: First token slow -> Fix: Streaming, small batches. 5) Throughput: Sequential requests -> Fix: Continuous Batching. Icons for each, red problem / green solution.",
  "file": "images/11_inference_opt/fig02_five_bottlenecks.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 72,
    "latex_width": "0.85\\textwidth",
    "caption": "Die fünf Engpässe der LLM-Inference mit Gegenmaßnahmen",
    "label": "fig:five-bottlenecks"
  }
}
```

### FIG 3: Inference Serving Stack
**Target:** Nach Zeile 111 (Serving Stack Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/11_inference_opt/fig03_serving_stack.pdf}`

```json
{
  "prompt": "Layered architecture: Inference Serving Stack. TOP: HTTP Client -> API Gateway -> Load Balancer. MIDDLE: Request Scheduler (Continuous Batching). BOTTOM: GPU Array [GPU 0: Llama][GPU 1: Llama][GPU 2: ...] each with KV-Cache. Arrows showing request flow. Kubernetes-style architecture diagram, clean boxes.",
  "file": "images/11_inference_opt/fig03_serving_stack.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 111,
    "latex_width": "0.9\\textwidth",
    "caption": "Architektur eines Inference-Servers: Client → Gateway → Scheduler → GPU Pool",
    "label": "fig:serving-stack"
  }
}
```

### FIG 4: PagedAttention Visualization
**Target:** Nach Zeile 123 (PagedAttention Description)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/11_inference_opt/fig04_pagedattention.pdf}`

```json
{
  "prompt": "Technical illustration: PagedAttention memory management. LEFT (Traditional): Contiguous KV-Cache blocks with fragmentation gaps (red). RIGHT (PagedAttention): Fixed-size pages (green blocks) mapped via page table, no fragmentation, copy-on-write sharing between sequences. Page 1/2/3. Page table visualization. Memory efficiency: 60% less fragmentation.",
  "file": "images/11_inference_opt/fig04_pagedattention.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 123,
    "latex_width": "0.85\\textwidth",
    "caption": "PagedAttention: Seitenbasierte KV-Cache-Verwaltung vermeidet Fragmentierung",
    "label": "fig:pagedattention"
  }
}
```

### FIG 5: Continuous Batching
**Target:** Nach Zeile 167 (Continuous Batching Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/11_inference_opt/fig05_continuous_batching.pdf}`

```json
{
  "prompt": "Timeline comparison: TOP (Without Continuous Batching): Req1 [====] Gap [====] Req2 [====] Gap [====] Req3. GPU Utilization ~50%. BOTTOM (With Continuous Batching): Req1 Req2 Req3 Req4 Req5 Req6 tightly packed, new requests fill gaps instantly. GPU Utilization ~95%. Time axis, colored blocks for requests, gaps shown.",
  "file": "images/11_inference_opt/fig05_continuous_batching.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 167,
    "latex_width": "0.9\\textwidth",
    "caption": "Continuous Batching: Ohne (50% Auslastung) vs. Mit (95% Auslastung)",
    "label": "fig:continuous-batching"
  }
}
```

### FIG 6: Quantization Formats
**Target:** Nach Zeile 197 (Quantization Table)
**LaTeX:** `\includegraphics[width=0.85\textwidth]{images/11_inference_opt/fig06_quantization_formats.pdf}`

```json
{
  "prompt": "Comparison chart: Quantization formats for 70B model. FP16/BF16 (16-bit, 140GB VRAM, Reference quality) -> INT8 (8-bit, 70GB, Minimal loss) -> INT4 GPTQ/AWQ (4-bit, 35GB, Slight loss) -> NF4 QLoRA (4-bit, 35GB, Slight loss) -> FP4 (4-bit, 35GB, Moderate loss). Bar chart for VRAM, quality degradation indicators. German labels.",
  "file": "images/11_inference_opt/fig06_quantization_formats.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 197,
    "latex_width": "0.85\\textwidth",
    "caption": "Quantisierungsformate: VRAM-Bedarf und Qualitätsverlust für 70B-Modell",
    "label": "fig:quant-formats"
  }
}
```

### FIG 7: Quality Loss by Task
**Target:** Nach Zeile 245 (Quality Loss Verbatim)
**LaTeX:** `\includegraphics[width=0.8\textwidth]{images/11_inference_opt/fig07_quality_loss_by_task.pdf}`

```json
{
  "prompt": "Horizontal bar chart: Quality loss by task type after INT4 quantization. General Chat (-2%), Summarization (-3%), Extraction (-2%), Code Generation (-5% to -15%), Math (-8% to -20%), Multi-step Reasoning (-10% to -25%). Color gradient green to red. Annotation: 'For 90% of production: INT4 AWQ sufficient. Code/Math: prefer INT8.'",
  "file": "images/11_inference_opt/fig07_quality_loss_by_task.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 245,
    "latex_width": "0.8\\textwidth",
    "caption": "Qualitätsverlust durch INT4-Quantisierung nach Aufgabentyp",
    "label": "fig:quality-loss"
  }
}
```

### FIG 8: Speculative Decoding
**Target:** Nach Zeile 264 (Speculative Decoding Verbatim)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/11_inference_opt/fig08_speculative_decoding.pdf}`

```json
{
  "prompt": "Two-flow diagram: NORMAL DECODE: Target Model (70B) -> Token 1 -> Target -> Token 2 -> Target -> Token 3 (slow, autoregressive). SPECULATIVE DECODING: Draft Model (1B) -> Tokens 1,2,3,4 (fast, parallel guess) -> Target Model (70B) verifies all 4 in ONE forward pass -> Accept/Reject -> 2-3x speedup. Same tokenizer requirement highlighted. Clean technical flow.",
  "file": "images/11_inference_opt/fig08_speculative_decoding.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 264,
    "latex_width": "0.9\\textwidth",
    "caption": "Speculative Decoding: Draft-Modell ratet, Target-Modell verifiziert in einem Forward-Pass",
    "label": "fig:speculative-decoding"
  }
}
```

### FIG 9: Performance Comparison
**Target:** Nach Zeile 327 (Performance Table)
**LaTeX:** `\includegraphics[width=0.9\textwidth]{images/11_inference_opt/fig09_performance_comparison.pdf}`

```json
{
  "prompt": "Grouped bar chart: Performance comparison for 70B on 4xA100. Four configurations: 1) FP16 No Batch: TTFT 1200ms, TPOT 65ms, Throughput 15 tok/s. 2) AWQ INT4 No Batch: TTFT 700ms, TPOT 35ms, Throughput 28 tok/s. 3) AWQ INT4 Cont. Batch(16): TTFT 900ms, TPOT 42ms, Throughput 180 tok/s. 4) AWQ INT4 + Spec Decode: TTFT 850ms, TPOT 18ms, Throughput 320 tok/s. Three metrics grouped per config.",
  "file": "images/11_inference_opt/fig09_performance_comparison.png",
  "metadata": {
    "chapter": "11_inferenz_optimierung",
    "insert_after_line": 327,
    "latex_width": "0.9\\textwidth",
    "caption": "Performance-Vergleich: FP16 vs AWQ INT4 vs Continuous Batching vs Speculative Decoding",
    "label": "fig:perf-comparison"
  }
}
```

---

## KAPITEL 12: CACHING, ROUTING, GUARDRAILS (12_caching_routing_guardrails.tex)

*Need to read this chapter first for exact line numbers*

---

## KAPITEL 13: MODELLANPASSUNG / FINE-TUNING (13_modellanpassung.tex)

*Need to read this chapter first*

---

## KAPITEL 14: MULTIMODALE KI (14_multimodale_ki.tex)

*Need to read this chapter first*

---

## KAPITEL 15: MLOPS OBSERVABILITY (15_mlops_observability.tex)

*Need to read this chapter first*

---

## KAPITEL 16: SECURITY GOVERNANCE (16_security_governance.tex)

*Need to read this chapter first*

---

## GENERATION WORKFLOW

```bash
# Für jedes Bild:
cd /Users/snow/dev/book/Become-an-AI-engineer
gemini-create-photo --prompt "$(cat images/07_rag/fig01_rag_pipeline_overview.prompt)" \
  --output images/07_rag/fig01_rag_pipeline_overview.png \
  --aspect 16:9 --style technical

# Dann in LaTeX einbinden:
# \begin{figure}[htbp]
#   \centering
#   \includegraphics[width=0.9\textwidth]{images/07_rag/fig01_rag_pipeline_overview.pdf}
#   \caption{RAG-System: Offline Indexing Pipeline (links) und Online Runtime Pipeline (rechts)}
#   \label{fig:rag-pipeline-overview}
# \end{figure}
```

---

## NAMING CONVENTION
```
fig{XX}_{chapter_short}_{descriptive_name}.png
```
- XX: 01, 02, 03... pro Kapitel
- chapter_short: rag, agents, inference_opt, caching, finetuning, multimodal, mlops, security
- descriptive_name: snake_case, kurz aber eindeutig

---

## EXPORT FORMATS
1. **PNG** für gemini-create-photo Output
2. **PDF** für LaTeX (convert: `magick fig.png fig.pdf` oder `inkscape fig.png --export-type=pdf`)
3. **SVG** optional für Web/HTML Export

Empfehlung: PNG generieren → ImageMagick zu PDF konvertieren → in LaTeX einbinden.