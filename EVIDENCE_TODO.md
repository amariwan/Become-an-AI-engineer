# Evidence Quality Fixes Needed

## Duplicated Claims (Need Single Deep Home + Forward Refs)

### 1. RAG E-Commerce Story ($450→$38, 67%→94%, 3.2s→800ms)
- **Deep Home**: Ch 7 (RAG) - KEEP FULL
- **Forward Refs Only**: Ch 11 (Inference), Ch 12 (Caching), Ch 14 (Multimodal)
- **Current**: Ch 7, 11, 12, 14 all have full story

### 2. Prompt Engineering Story ($400→$12, 61%→94%)
- **Deep Home**: Ch 6 (Prompt Design) - KEEP FULL
- **Forward Refs Only**: Ch 1 (Role), Ch 4 (OpenAI - removed), Ch 8 (Agents)
- **Current**: Ch 1, Ch 4 (removed), Ch 6, Ch 8

### 3. Token Budget Story ($400→$12, 2000→8000 convos)
- **Deep Home**: Ch 5 (Token Mgmt) - KEEP FULL (SupportPilot)
- **Forward Refs**: Ch 8 (Agents), Ch 12 (Caching), Ch 16 (Security)

### 4. Agent Runaway Story ($400 in 4 min)
- **Deep Home**: Ch 8 (Agents) - KEEP FULL
- **Forward Refs**: Ch 12 (Caching/Budget), Ch 16 (Security)

### 5. Prompt JSON Validity (67%→94%)
- **Deep Home**: Ch 6 (Prompt) - KEEP FULL
- **Forward Refs**: Ch 4 (OpenAI), Ch 7 (RAG), Ch 8 (Agents), Ch 9 (Eval)

## Evidence Frameworks Needed for Each Number

For EVERY quantitative claim, add measurement framework:
- Metric definition
- Baseline (what was measured before)
- Dataset (what data, size, source)
- n (sample size) or why unavailable
- What changed (the intervention)
- Limitations/assumptions

## Timelessness Fixes Needed

### Year References in Prose (move to tables/footnotes):
- Ch 1: "2020: Model Training. 2024: Model Integration" → "Phase 1: Model Training. Phase 2: Model Integration"
- Ch 1: "2021-2024" startup dates → "recent years"
- Ch 1: "2023-heute" → "current phase"
- Ch 1: "2023+ Gegenwart" → "current phase"
- Ch 1: "gpt-4o-2026-03-15" → move to table with footnote
- Ch 2: "2023-heute" → "current phase"
- Ch 2: "Cutoff 2024" → "recent cutoff"
- Ch 2: "gpt-4o-2026-01-15" → table with footnote
- Ch 3: "gpt-4o-2026-03-15" → table with footnote
- Ch 4: "gpt-4o-2026-03-15" → table with footnote
- Ch 5: "Juli 2025" prices → "Stand der Ausgabe" footnote
- Ch 7: "2024-01-15" date → remove or footnote
- Ch 7: "2022 vs 2024" embedding → "older vs newer" with footnote

### Model Names in Prose (move to tables):
- "GPT-4o", "Claude 4", "Gemini 2.5", "Llama 4" in prose → move to comparison tables with date footnotes
- Keep "large reasoning model" or "current flagship model" in prose

## Provider-Agnostic Fixes

Replace in prose:
- "OpenAI" → "API provider" or "provider"
- "OpenAI API" → "Chat Completions API"
- "Anthropic" → "provider" (keep in tables)
- "Anthropic API" → "Messages API"
- "Google" / "Gemini" → "provider" (keep in tables)

## Unique Production Stories Needed

### Ch 1 (Role): Already has Claypot story ✓
### Ch 2 (Models): Already has automotive/healthcare/ecommerce ✓  
### Ch 3 (Landscape): Already has SaaS/Automotive/Fintech ✓
### Ch 4 (OpenAI): REMOVED from TOC ✓
### Ch 5 (Token): SupportPilot ✓
### Ch 6 (Prompt): SupportPilot prompt journey ✓
### Ch 7 (RAG): E-Commerce RAG ✓
### Ch 8 (Agents): SupportPilot multi-agent ✓
### Ch 9 (Eval): SupportPilot eval journey ✓
### Ch 10 (Deployment): SupportPilot v1→v4 ✓
### Ch 11 (Inference): NEEDS NEW STORY - Self-hosting SupportPilot for PII
### Ch 12 (Cache/Routing): SupportPilot FAQ cache + intent router ✓
### Ch 13 (Fine-tuning): NEEDS NEW STORY - SupportPilot SQL expert
### Ch 14 (Multimodal): NEEDS NEW STORY - SupportPilot screenshot/document analysis
### Ch 15 (MLOps): NEEDS NEW STORY - SupportPilot model drift incident
### Ch 16 (Security): SupportPilot agent file deletion incident ✓

## Action Plan

1. Fix duplicated claims (keep deep home, add forward refs)
2. Add evidence frameworks to all remaining numbers
3. Remove timelessness violations
4. Make provider-agnostic
5. Verify unique stories per chapter
5. Run quality gate