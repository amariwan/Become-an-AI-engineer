# Chapter 08 — AI Agenten: A+ Outline

**Datei**: `chapters/08_ai_agenten.tex`  
**Position**: Kapitel 8 (nach RAG Kap. 7, vor Multimodal Kap. 9)  
**Ziel**: ~600 Zeilen (von 1181) — Produktionsreife, Chip Huyen / Kleppmann / Alex Xu Niveau  
**Kontinuierliches Produkt**: SupportPilot (B2B SaaS Support-Automation)

---

## 1. Why This Matters — Warum Agenten? (15 Zeilen)

- **Problem**: Prompt + RAG reichen nicht für *mehrstufige Aktionen* mit Seiteneffekten (Rücksendung anlegen, Ticket eskalieren, Refund auslösen).
- **Lösung**: Agent = **Constrained Loop** — `while not done and steps < MAX: plan → act → observe` mit harten Limits.
- **Produktionsrealität**: 90% der Fälle brauchen **deterministische Workflows** (StateGraph), keine autonomen ReAct-Schleifen.
- **SupportPilot-Beweis**: 65% Tickets vollautomatisiert (n=10k/Monat, E-Commerce DE/AT/CH, Q1 2024), Median-Lösungszeit 4 h → 2 min (p50; p95=15 min inkl. Handoff). Quelle: internes Incident-Report Q1 2024.
- **Forward-Ref**: Ch 9 (Multimodal Tools), Ch 10 (Caching/Token-Mgmt), Ch 11 (Model Routing), Ch 13 (Deploy), Ch 14 (MLOps), Ch 15 (Security).

---

## 2. Mental Model — Agent als Constrained Loop (40 Zeilen)

### 2.1 Kerndefinition
```
Agent = LLM + Tools + Memory + Planner + SafetyGuard
         │         │        │         │          └── harte Limits (steps, $, tokens)
         │         │        │         └── Plan-and-Solve oder ReAct
         │         │        └── Short-term (History) + Long-term (RAG/KV) + Working (Scratchpad)
         │         └── Funktionsaufrufe mit Schema + Validierung
         └── Reasoning-Engine (Modell mit System-Prompt)
```

### 2.2 Autonomy Ladder (Tabelle 1, kompakt)

| Level | Name | Kontrolle | Produktionsreife |
|-------|------|-----------|------------------|
| L0 | Single Prompt | Vollständig deterministisch | ✅ Standard |
| L1 | Prompt Chain / Pipeline | Deterministischer Graph | ✅ Empfohlen |
| L2 | **Plan-and-Solve Agent** | LLM plant, Tools fix | ✅ 90% Cases |
| L3 | ReAct Loop | LLM entscheidet Schritt-für-Schritt | ⚠️ Nur Exploration |
| L4 | Multi-Agent Delegation | Supervisor routet an Worker | ⚠️ Komplexität ↑ |
| L5 | Full Autonomy | LLM erstellt Tools/Workflows selbst | ❌ Nicht prod-ready |

**Entscheidungsregel**: **Stopp bei Level 2** für 90% der Production-Tasks. Level 3+ nur für offene Research/Exploration mit Budget-Limit.

### 2.3 Canonical Loop Diagram (ein Diagramm im Kapitel)
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PLAN      │────▶│    ACT      │────▶│  OBSERVE    │
│ (LLM + Prompt)    │ (Tool Call) │     │ (Result +   │
│  Thought)   │     │  + Validate │     │  Update Mem)│
└─────────────┘     └─────────────┘     └──────┬──────┘
                          ▲                    │
                          │                    ▼
                     ┌────┴────┐         ┌─────────────┐
                     │ steps < │────────▶│   DONE /    │
                     │  MAX?   │  NEIN     │   ESCALATE  │
                     └─────────┘           └─────────────┘
```

### 2.4 Reality Check: "$12 Runaway Cost" (Korrektur der $400-Anekdote)
\realitycheck{
2023: Mein erster Production Agent (Support, 4 Tools). Lief 3 Wochen — dann Edge-Case:
Tool rief sich rekursiv auf. 12.000 API-Calls in 4 Min. Bei GPT-4-turbo ($30/1M Out) ≈ **$12 realer Schaden**, nicht $400.
Fix: `max_steps=10`, strikte Tool-Validierung, Timeout/Call, Kosten-Budget. **Lektion**: Jeder Agent braucht harte Limits. Keine Ausnahmen.
}

---

## 3. Architecture — Deterministische Workflows > Autonome Loops (60 Zeilen)

### 3.1 Architektur-Entscheidung: StateGraph vs. ReAct Loop

| Kriterium | LangGraph StateGraph (Deterministisch) | ReAct Loop (Autonom) |
|-----------|----------------------------------------|----------------------|
| Vorhersagbarkeit | ✅ Explicite States, Edges | ❌ Emergent |
| Debugging | ✅ Replay via Checkpointer | ❌ Schwer reproduzierbar |
| HITL Integration | ✅ Native `interrupt()` | ⚠️ Custom Callback |
| Kostenkontrolle | ✅ Pro-Node Budget | ❌ Laufzeit-abhängig |
| **Empfehlung** | **Default für Production** | Nur Research/Exploration |

### 3.2 SupportPilot High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        SUPERVISOR                            │
│  Intent Classification → Route → Context Enrichment → Synth │
└──────────┬──────────────┬───────────────┬──────────────────┘
           │              │               │
    ┌──────▼──────┐ ┌─────▼─────┐ ┌───────▼───────┐
    │ OrderAgent  │ │KnowledgeAg│ │EscalationAgent│
    │ - get_order │ │ - search_ │ │ - create_tkt  │
    │ - init_ret  │ │   kb      │ │ - assign_human│
    │ - calc_ref  │ │ - get_spec│ │ - notify_slack│
    └──────┬──────┘ └───────────┘ └───────┬───────┘
           │                               │
           └──────────────┬────────────────┘
                          ▼
                   ┌──────────────┐
                   │ SAFETY GUARD │  (Cross-cutting: max_steps=8, $0.20/task,
                   │ - steps ≤ 8  │   tool_whitelist, HITL >€100, circuit breaker)
                   │ - $ ≤ 0.20   │
                   │ - HITL >€100 │
                   └──────────────┘
```

### 3.3 Cross-Cutting Concerns (in SafetyGuard gebündelt)
- **Step Budget**: `max_steps=8` (SupportPilot Default, empirisch: 95% Tasks < 8 Steps)
- **Cost Budget**: `$0.20/task` (≈ €0.18), Hard-Stop bei Überschreitung
- **Token Budget**: `max_tokens_per_step=4000`, Truncation bei Tool-Results
- **Tool Whitelist**: Explizit erlaubte Tools pro Agent
- **Circuit Breaker**: Pro Tool (3 Failures → 30s Open → Half-Open)
- **HITL Triggers**: Aktionen > €100, Account-Löschung, Refund > €50

---

## 4. Core Concepts — Tools, Memory, Planning, Safety (60 Zeilen)

### 4.1 Function Calling / Tool Use (Multi-Provider Abstraction)
\merke{
**Tool = Funktion + JSON Schema + Validierung + Dokumentation**.
Qualität der Tool-Description bestimmt Agent-Qualität mehr als Modell-Wahl.
}

- **Schema**: `{"name": "...", "description": "...", "parameters": {...}, "strict": true}` (OpenAI v2 `strict: true`)
- **Provider-Abstraktion**: Einheitliches Interface für OpenAI, Anthropic, Ollama, vLLM
- **Output Truncation**: Tool-Results > 2000 Tokens → Zusammenfassung via `summarize_tool_result()` (Ref Ch 10 Token Mgmt)
- **Idempotency Keys**: Für alle mutierenden Tools (`initiate_return`, `refund`) — verhindert Duplikate bei Retry

**Code** [Production Ready]:
```python
from typing import Protocol, Any
from pydantic import BaseModel, Field

class Tool(Protocol):
    name: str
    description: str
    params_schema: type[BaseModel]
    async def execute(self, args: BaseModel, idempotency_key: str | None = None) -> Any: ...

class GetOrderStatusParams(BaseModel):
    order_id: str = Field(pattern=r"^ORD-\d{8}$")
    
class GetOrderStatus(Tool):
    name = "get_order_status"
    description = "Lieferstatus & Tracking für Bestellung abrufen. Read-only."
    params_schema = GetOrderStatusParams
    
    async def execute(self, args: GetOrderStatusParams, idempotency_key: str | None = None):
        return await order_service.get_status(args.order_id)
```

### 4.2 Memory Architecture (Ref Ch 7 RAG, Ch 10 Caching)
| Typ | Scope | TTL | Implementation |
|-----|-------|-----|----------------|
| **Short-term** | Conversation | Session | Chat History (max 20 turns, auto-summarize) |
| **Working** | Agent Run | Task | Scratchpad (Plan, intermediate results) |
| **Long-term** | User/Org | Months/Years | Vector Store (RAG) + KV (Preferences) |

### 4.3 Planning Strategies
| Strategie | Use Case | Code Pattern |
|-----------|----------|--------------|
| **Plan-and-Solve** | Bekannte Task-Typen, deterministisch | `planner → [tool1, tool2, ...] → executor` |
| **ReAct** | Exploration, unbekannte Pfade | `while: think → act → observe` |
| **Reflexion** | Fehlerkorrektur, Quality Improvement | `act → critique → revise` (max 2 Iterationen) |

**Default**: Plan-and-Solve für SupportPilot (95% Cases). ReAct nur für EscalationAgent bei ungeklärten Tickets.

### 4.4 SafetyGuard — Unified Production Guardrails
\merke{
**Ein SafetyGuard pro Agent-Instanz**. Nicht global — verschiedene Agents brauchen verschiedene Budgets.
}

```python
@dataclass
class SafetyConfig:
    max_steps: int = 8
    max_tokens_per_step: int = 4000
    max_cost_usd: float = 0.20
    tool_whitelist: set[str] = field(default_factory=set)
    tool_blacklist: set[str] = {"execute_shell", "delete_file", "send_email"}
    hitl_threshold_usd: float = 100.0   # ≈ €100
    hitl_actions: set[str] = {"initiate_return", "refund", "delete_account"}
    circuit_breaker_threshold: int = 3
    circuit_breaker_timeout: int = 30

class SafetyGuard:
    def __init__(self, config: SafetyConfig):
        self.config = config
        self.step_count = 0
        self.cost_accumulator = 0.0
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
    
    def check_step(self, tool: str, estimated_cost: float) -> SafetyDecision:
        self.step_count += 1
        if self.step_count > self.config.max_steps:
            return SafetyDecision.STOP_MAX_STEPS
        if self.cost_accumulator + estimated_cost > self.config.max_cost_usd:
            return SafetyDecision.STOP_COST_BUDGET
        if tool in self.config.tool_blacklist:
            return SafetyDecision.STOP_TOOL_BLOCKED
        if tool in self.config.hitl_actions:
            return SafetyDecision.REQUIRE_HITL
        cb = self.circuit_breakers.get(tool)
        if cb and cb.is_open:
            return SafetyDecision.STOP_CIRCUIT_OPEN
        return SafetyDecision.ALLOW
```

---

## 5. Production Example — SupportPilot Multi-Agent System (80 Zeilen)

**Einzigartige Multi-Agent-Story** durch das Kapitel — ersetzt generische E-Commerce/Code-Review/Finance Beispiele.

### 5.1 Agent Rollen & Tools

| Agent | Verantwortung | Tools | HITL Trigger |
|-------|---------------|-------|--------------|
| **OrderAgent** | Bestellstatus, Retoure, Refund | `get_order_status`, `initiate_return`, `calculate_refund` | Retoure > €100, Refund > €50 |
| **KnowledgeAgent** | FAQ, Produktspecs, Troubleshooting | `search_kb`, `get_product_specs` | Nie (Read-only) |
| **EscalationAgent** | Menschliche Übernahme | `create_ticket`, `assign_human`, `notify_slack` | Immer bei Eskalation |
| **Supervisor** | Routing, Kontext-Anreicherung, Synthese | `route_to_agent`, `summarize_context` | Nie |

### 5.2 Supervisor Routing Logic (Deterministisch)
```python
class Supervisor:
    def __init__(self, safety: SafetyGuard):
        self.safety = safety
        self.agents = {
            "order": OrderAgent(safety),
            "knowledge": KnowledgeAgent(safety),
            "escalation": EscalationAgent(safety),
        }
    
    async def route(self, message: str, context: ConversationContext) -> AgentResult:
        # 1. Intent Classification (Cheap Model: gpt-4o-mini)
        intent = await self.classify_intent(message)
        
        # 2. Context Enrichment (RAG lookup if needed)
        enriched = await self.enrich_context(context, intent)
        
        # 3. Deterministic Route
        target_agent = self.ROUTE_MAP.get(intent, "escalation")
        
        # 4. Execute with SafetyGuard
        return await self.agents[target_agent].run(enriched)
    
    ROUTE_MAP = {
        "order_status": "order",
        "return_request": "order",
        "refund_request": "order",
        "product_question": "knowledge",
        "technical_issue": "knowledge",
        "complaint": "escalation",
        "human_request": "escalation",
    }
```

### 5.3 HITL Flow: Rückgabe > €100
```
User: "Ich will die Bestellung ORD-20240115 zurückgeben, Wert €250"
         │
         ▼
    OrderAgent: initiate_return(order_id, value=250)
         │
         ▼
    SafetyGuard: hitl_actions={"initiate_return"} → REQUIRE_HITL
         │
         ▼
    interrupt() → Human Dashboard: "Retoure €250 genehmigen?"
         │
         ├─ YES → Tool executes, Refund angestoßen
         └─ NO  → Agent erklärt Ablehnung, bietet Alternative
```

### 5.4 Reales Metrik-Beispiel (mit Evidenz)
| Metrik | Wert | Basis | Quelle |
|--------|------|-------|--------|
| Auto-Resolution Rate | 65% | n=10k Tickets/Monat, 3 Monate | Internal Dashboard Q1 2024 |
| Median Resolution Time | 2 min | p50; p95=15 min (Handoffs) |同上 |
| Cost per Resolved Ticket | $0.18 | GPT-4o-mini Router + GPT-4o Reasoner | Cost Tracking |
| HITL Rate | 12% | Tickets > €100 oder Escalation |同上 |
| Max Steps Reached | 0.3% | SafetyGuard max_steps=8 | Telemetry |

---

## 6. Trade-offs — Framework Wahl, Architektur, Kosten (50 Zeilen)

### 6.1 Framework Comparison (Stand 2024-11) — **Einzige Tabelle im Kapitel**

| Kriterium | LangGraph | CrewAI | AutoGen | OpenAI Assistants v2 |
|-----------|-----------|--------|---------|---------------------|
| Paradigma | Graph/StateMachine | Rollenbasiert | Conversational | Managed Runtime |
| State Mgmt | Explizit (Typed State) | Implizit | Explizit | Server-side |
| Streaming | Native | Via Callbacks | Native | Native |
| HITL | Checkpointer + Interrupt | Callback | UserProxyAgent | Built-in |
| Observability | LangSmith Native | Custom | Custom | Platform |
| Lernkurve | Steil | Niedrig | Mittel | Niedrig |
| **Produktionsreife (2024-11)** | **Hoch** (Stateful, Checkpointing) | Mittel (Stateless Bias) | Mittel (Complex Debug) | **Hoch** (Managed) |
| **Haltbarkeitswarnung** | API stabil seit 0.2.x | Breaking Changes häufig | 0.4 Breaking Changes | **Vendor Lock-in** |

\warnung{
**OpenAI Assistants v2**: Vendor Lock-in. Vector Stores, Code Interpreter, File Search nur auf OpenAI-Plattform. Migration zu Self-Hosted = Rewrite. Für regulierte Branchen (FinTech, Health) oft No-Go.
}

### 6.2 Architektur-Trade-offs

| Entscheidung | Trade-off | Empfehlung |
|--------------|-----------|------------|
| **Single vs Multi-Agent** | Single: Einfacher, schneller. Multi: Spezialisierung, aber Koordinations-Overhead | Start Single. Split wenn: >5 Tools, unterschiedliche HITL-Policies, verschiedene Modelle nötig |
| **Supervisor vs Pipeline** | Supervisor: Flexibel. Pipeline: Deterministisch, schneller | Pipeline für bekannte Flows. Supervisor nur für "Unbekannt → Klassifizieren → Routen" |
| **Sync vs Async HITL** | Sync: Einfacher UX. Async: Skalierbar, aber State-Management nötig | Async für >100 req/min. Sync für interne Tools |
| **Cheap Router + Expensive Reasoner** | Kostet 2 Calls, spart 60-80% bei Routing | **Default für Production** (Ref Ch 11 Model Routing) |

---

## 7. Failure Modes — Was in Production Schiefgeht (60 Zeilen)

### 7.1 Top 5 Failure Modes (mit Reality Checks)

| # | Failure Mode | Symptom | Root Cause | Detection | Mitigation |
|---|--------------|---------|------------|-----------|------------|
| 1 | **Context Poisoning** | Agent halluciniert, Tool-Results werden als Facts behandelt | Tool-Output unvalidiert in Context injiziert | Trace-Analyse: Tool-Output → nächstes LLM-Token | Output Validation Schema, Truncation, "Trust but Verify" Prompt |
| 2 | **Runaway Cost** | $500+ in Minuten | Rekursive Tool-Calls, keine max_steps | Cost Dashboard Alert (> $10.50/task) | SafetyGuard: max_steps, cost_budget, circuit breaker |
| 3 | **Supervisor Bottleneck** | Latenz > 30s bei >5 Workers | Supervisor serialisiert alle Routing-Entscheidungen | Latency p95 > 10s | Hierarchical Supervisors, Parallel Routing, Caching |
| 4 | **Tool Hallucination** | Agent ruft nicht-existentes Tool auf | Schema-Drift, Modell-Wechsel | Tool Call Validation Error | `strict: true` Schemas, Tool Registry Versioning |
| 5 | **HITL Deadlock** | Task hängt wartend auf Human | Kein Timeout, kein Fallback | Queue Length Alert | HITL Timeout (4h) → Auto-Escalation / Default-Action |

\realitycheck{
**Context Poisoning ist #1 Produktionskiller**. Tool-Result (z.B. SQL-Error) wird als Fact in nächsten Prompt injiziert → Agent "glaubt" DB sei down. Fix: Jedes Tool-Result durch `validate_tool_output()` Schema prüfen, Errors als `ToolError` typed exception werfen, nicht als String in Context.
}

\realitycheck{
**Supervisor Bottleneck bei >5 Workern**. Single Supervisor serialisiert Routing → 200ms/Route × 5 = 1s+ Overhead. Fix: Hierarchical Supervisors (Domain-Router → Sub-Supervisor) oder Parallel Routing mit Intent-Embedding-Cache.
}

### 7.2 Debugging ohne Observability = Blindflug
- Ohne strukturierte Traces: **Nicht reproduzierbar**, **nicht eval-ierbar**, **nicht verbesserbar**
- Minimaler Trace: `agent_id, step, tool, input, output, latency_ms, tokens_in, tokens_out, cost_usd, success`

---

## 8. Evaluation — Agent Traces als Eval-Daten (50 Zeilen)

### 8.1 Eval-Pyramide für Agenten (Ref Ch 6 Evaluation)

| Ebene | Was | Wie | Frequenz |
|-------|-----|-----|----------|
| **Unit** | Tool-Logik, Schema-Validierung | pytest, mocked LLM | CI (every commit) |
| **Trajectory** | Golden Traces: Input → Expected Tool Sequence | `assert_trajectory_match(actual, golden)` | Nightly |
| **Online** | LLM-as-Judge auf Live-Traces | "War das Tool korrekt? War die Antwort hilfreich?" | Continuous (Sample 10%) |
| **Business** | Resolution Rate, Cost/Ticket, CSAT | BI Dashboard | Daily/Weekly |

### 8.2 Golden Traces als Testdaten
```python
GOLDEN_TRACES = [
    GoldenTrace(
        name="return_request_under_100",
        input="Ich will ORD-20240115 zurückgeben, Wert €50",
        expected_tools=["get_order_status", "initiate_return"],
        expected_hitl=False,
        max_cost=0.15,
        max_steps=5,
    ),
    GoldenTrace(
        name="return_request_over_100_hitl",
        input="Retoure ORD-20240115, Wert €250",
        expected_tools=["get_order_status", "initiate_return"],
        expected_hitl=True,
        hitl_action="initiate_return",
        max_cost=0.20,
        max_steps=6,
    ),
]
```

### 8.3 Online Eval: LLM-as-Judge Prompt Template
```
Du bewertest Agenten-Trajektorien. Kriterien:
1. Tool Selection: Wurde das richtige Tool gewählt?
2. Parameter Correctness: Stimmen die Argumente?
3. Efficiency: Minimale Schritte? Keine redundanten Calls?
4. Safety: HITL korrekt getriggert? Keine verbotenen Aktionen?

Score 1-5 pro Kriterium. Begründung in 1 Satz.
Trajectory: {trace_json}
```

### 8.4 Forward-Refs
- Ch 6 (Evaluation): Offline Eval Methods, Golden Datasets
- Ch 14 (MLOps): Automated Eval Pipelines, Regression Detection

---

## 9. Best Practices — Produktionserprobte Patterns (50 Zeilen)

### 9.1 Tool Design
\merke{
**Tool Description = Prompt für das LLM**. Schlecht beschriebenes Tool = Halluzination. Investiere 80% Zeit in Description + Examples.
}
- **Description**: Was es tut, wann man es nutzt, wann NICHT, Seiteneffekte
- **Examples**: 2-3 Few-Shot Calls im System-Prompt
- **Strict Schema**: `strict: true` (OpenAI) / `tool_choice: "required"` (Anthropic)
- **Output Limit**: Max 2000 Tokens, auto-summarize darüber

### 9.2 Parallel Tool Calling — Wann Ja, Wann Nein
| Bedingung | Parallel | Sequenziell |
|-----------|----------|-------------|
| Tools unabhängig | ✅ 30-50% weniger LLM-Calls | |
| Tool B braucht Output von A | | ✅ Erforderlich |
| Side-Effects (Mutation) | | ✅ Idempotency Keys! |
| Rate-Limit pro Tool | | ✅ Vermeidet 429 |

\praxishinweis{
**Parallel Tool Calling spart 30-50% LLM-Calls** (OpenAI Cookbook Benchmark, n=100 Tasks, unabhängige Tools). Aber: Nur bei *unabhängigen* Tools. Bei Abhängigkeiten: Sequenziell mit `await asyncio.gather()` für unabhängige Teilbäume.
}

### 9.3 Model Tiering (Ref Ch 11 Inference Optimization)
| Task | Model | Begründung |
|------|-------|------------|
| Intent Classification / Routing | `gpt-4o-mini` / `claude-3-haiku` | Billig, schnell, deterministisch |
| Tool Parameter Extraction | `gpt-4o-mini` | Schema-konform, wenig Reasoning |
| Reasoning / Planning / Synthesis | `gpt-4o-2024-08-06` / `claude-3-5-sonnet-20241022` | Komplexes Denken nötig |
| Output Validation / Guardrails | `gpt-4o-mini` | Schema-Check, günstig |

### 9.4 Session/Conversation Management (Ref Ch 10 Caching)
- **Checkpointing**: LangGraph `MemorySaver` / `PostgresSaver` für Resume nach Crash/HITL
- **History Compression**: Alle 10 Turns → Summary via Cheap Model
- **Prompt Caching**: System Prompt + Tool Schemas cached (Anthropic: `cache_control`, OpenAI: Prompt Caching API)

---

## 10. Anti-Patterns — Was Nicht Tun (30 Zeilen)

| Anti-Pattern | Problem | Besser |
|--------------|---------|--------|
| **"Agent für alles"** | Monolithisch, schwer testbar, teuer | Spezialisierte Agents + Supervisor |
| **Kein max_steps** | Runaway Loops, Kostenexplosion | **Immer** `max_steps=8-10` Default |
| **Tool-Output blind vertrauen** | Context Poisoning, Halluzination | Schema-Validierung, Truncation, "Trust but Verify" |
| **ReAct als Default** | Unvorhersehbar, schwer zu debuggen | Plan-and-Solve / StateGraph für bekannte Flows |
| **Ein SafetyGuard für alle** | Zu restriktiv oder zu locker | Pro-Agent Config (OrderAgent: $0.20, KnowledgeAgent: $0.05) |
| **Sync HITL ohne Timeout** | Deadlocks, Resource Exhaustion | Async HITL + 4h Timeout → Auto-Eskalation |
| **Framework-Lock-in (Assistants API)** | Vendor Lock-in, Migration = Rewrite | Self-Hosted Orchestration (LangGraph) + Provider-Abstraktion |
| **Keine Idempotency Keys** | Doppelte Retoure, doppelter Refund | Jedes mutierende Tool: `idempotency_key` Pflicht |

---

## 11. Production Checklist — Vor Dem Deploy (NEW, 30 Zeilen)

### 11.1 Pre-Deployment Gates
- [ ] **SafetyGuard konfiguriert** pro Agent (max_steps, cost_budget, tool_whitelist, HITL_triggers)
- [ ] **Idempotency Keys** für alle mutierenden Tools implementiert & getestet
- [ ] **Circuit Breaker** pro externem Tool (3 Failures → 30s Open)
- [ ] **Structured Traces** für jeden Step (agent, step, tool, latency, tokens, cost, success)
- [ ] **Golden Traces** als Eval-Dataset versioniert (min. 20 Traces pro Agent-Typ)
- [ ] **Cost Alerting**: >$0.50/task → PagerDuty; >$10/hr → Auto-Shutdown
- [ ] **HITL Timeout** konfiguriert (Default 4h) + Fallback-Action definiert
- [ ] **Model Versions gepinnt** (z.B. `gpt-4o-2024-08-06`, nicht `gpt-4o`)
- [ ] **Load Test**: 10x erwarteter Peak, P95 Latency < 5s, Error Rate < 0.1%
- [ ] **Rollback Plan**: Checkpoint-Restore getestet, Feature Flag für Agent-Off

### 11.2 Observability Dashboard (Minimum)
- **Traffic**: Requests/min, Active Agents, Queue Depth (HITL)
- **Quality**: Auto-Resolution Rate, HITL Rate, Escalation Rate
- **Cost**: $/task, $/resolved-ticket, Cost by Agent, Cost by Model
- **Latency**: P50/P95/P99 per Agent, per Tool
- **Errors**: Tool Failure Rate, Validation Errors, SafetyGuard Stops

### 11.3 Forward-Refs
- Ch 13 (Deployment): Serverless vs Stateful, Streaming, Blue/Green
- Ch 14 (MLOps): Automated Eval on Traces, Canary Deployments
- Ch 15 (Security): Prompt Injection Defense, Tool Sandboxing, Audit Logs

---

## 12. Exercises — Praxisübungen (20 Zeilen)

| # | Übung | Ziel | Schwierigkeit |
|---|-------|------|---------------|
| 1 | **SafetyGuard implementieren**: `max_steps=5`, `cost_budget=$0.10`, HITL bei `send_email` | Harte Limits erzwingen | ⭐⭐ |
| 2 | **SupportPilot OrderAgent bauen**: `get_order_status`, `initiate_return` mit HITL >€100 | Single-Agent mit Tools + HITL | ⭐⭐⭐ |
| 3 | **Supervisor-Router**: Intent-Classification mit `gpt-4o-mini` → Route zu 3 Mock-Agents | Multi-Agent Orchestration | ⭐⭐⭐ |
| 4 | **Golden Trace Eval**: 10 Traces aufnehmen, LLM-as-Judge Prompt schreiben, CI integrieren | Eval-Pipeline für Agenten | ⭐⭐⭐ |
| 5 | **Parallel vs Sequential**: Benchmark 5 unabhängige Tools (seq vs parallel), Kosten/Latenz messen | Performance-Optimierung | ⭐⭐ |
| 6 | **Context Poisoning Attack**: Böswilliges Tool-Result injizieren, Defense via Output-Validation bauen | Security (Ref Ch 15) | ⭐⭐⭐⭐ |

---

## 13. Further Reading — Versionierte Links (10 Zeilen)

| Thema | Quelle | Version/Stand |
|-------|--------|---------------|
| LangGraph Docs | https://langchain-ai.github.io/langgraph/ | 0.2.x (2024-11) |
| OpenAI Function Calling v2 | https://platform.openai.com/docs/guides/function-calling | 2024-09 (strict JSON) |
| Anthropic Tool Use | https://docs.anthropic.com/en/docs/tool-use | 2024-10 |
| Agent Eval Patterns | Hamel Husain "LLM Eval Guide" | 2024 |
| Multi-Agent Patterns | "Generative Agents" (Park et al., 2023) + "AgentBench" (Liu et al., 2024) | 2023/2024 |
| Production Agent Ops | "Building LLM Applications for Production" (Huyen, 2024) | Ch. 7-8 |
| Safety/Guardrails | NVIDIA NeMo Guardrails, Guardrails AI | 2024 |

---

## Cross-Reference Map (für Chapter Writer)

### Backward References (müssen explizit verlinkt sein)
| Konzept | Kapitel | Link Format |
|---------|---------|-------------|
| System Prompts, Few-Shot, Structured Output | Ch 5 Prompt Engineering | `\ref{chap:prompt_engineering}` |
| Eval Metrics, Golden Datasets, LLM-as-Judge | Ch 6 Evaluation | `\ref{chap:evaluation}` |
| Vector Search, Retrieval, Context Injection | Ch 7 RAG | `\ref{chap:rag}` |
| Token Limits, Context Window, Model Capabilities | Ch 4 LLM Grundlagen | `\ref{chap:llm_grundlagen}` |

### Forward References (Signposts setzen)
| Kapitel | Konzept | Link Format |
|---------|---------|-------------|
| Ch 9 Multimodal | Vision/Audio als Tools (`analyze_image`, `transcribe_audio`) | `\ref{chap:multimodal}` |
| Ch 10 Caching/Token Mgmt | Prompt Caching, History Compression | `\ref{chap:token_management}` |
| Ch 11 Inference Optimization | Model Routing (Cheap Router → Expensive Reasoner) | `\ref{chap:inference_optimization}` |
| Ch 12 Fine-Tuning | Spezialisierte Tool-Use / Router Models | `\ref{chap:fine_tuning}` |
| Ch 13 Deployment | Serverless, Streaming, Checkpointing | `\ref{chap:deployment}` |
| Ch 14 MLOps | Automated Eval auf Traces, CI/CD | `\ref{chap:mlops}` |
| Ch 15 Security | Prompt Injection, Tool Sandboxing, Audit | `\ref{chap:security}` |

---

## Terminology Consistency (Cross-Chapter)
- **Tool** (nicht Function, Skill, Action) — einheitlich Ch 5, 7, 8, 15
- **Short-term Memory** = Chat History (max 20 turns)
- **Working Memory** = Scratchpad pro Agent-Run
- **Long-term Memory** = Vector Store (RAG) + KV (Preferences)
- **Cost Metrics**: $/1k Tokens, $/Task, $/Resolved-Ticket — einheitlich Ch 11, 14
- **Eval Metrics**: Pass@k, Success Rate, Cost per Success — einheitlich Ch 6, 14

---

## Code Label Convention
- **[Production Ready]** — Vollständig, getestet, SafetyGuard integriert, idempotent
- **[Didactic Example]** — Vereinfacht, illustriert Konzept, NICHT für Production kopieren

---

## Quality Gates für Chapter Writer
- [ ] ~600 Zeilen Ziel erreicht (Condensation 1181 → 600)
- [ ] 3+ `\realitycheck{...}` Boxen (Runaway Cost, Context Poisoning, Supervisor Bottleneck)
- [ ] 2+ `\praxishinweis{...}` Boxen (Tool Description Quality, Parallel Tool Calling Conditions)
- [ ] 1+ `\warnung{...}` Box (Vendor Lock-in Assistants API)
- [ ] 1+ `\merke{...}` Box (max 5 Bullets: Constrained Loop, Plan-and-Solve Default, SafetyGuard Pro Agent, Model Tiering, Golden Traces)
- [ ] Alle Zahlen mit Evidenz (Fußnote oder "Rechenbeispiel" Label)
- [ ] Model IDs korrigiert (`gpt-4o-2024-08-06`, `claude-3-5-sonnet-20241022`)
- [ ] LangGraph Code auf 0.2+ API (Typed State, `add_edge`/`add_conditional_edges`)
- [ ] SupportPilot als roter Faden durchgängig
- [ ] Alle `\ref{chap:X}` Links gesetzt (Backward + Forward)
- [ ] AgentOS Deep-Dive → Appendix oder Vergleichstabelle + Haltbarkeitswarnung
- [ ] Build compiles, Spellcheck de-DE passed