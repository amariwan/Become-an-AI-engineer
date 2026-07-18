Vollständiges Buch-Review
Become an AI Engineer — gelesen als Chip Huyen

Umfang: 16 Kapitel + Appendix + Glossar · ~44k Wörter · ~12k Zeilen LaTeX
Maßstab: AI Engineering / Designing Machine Learning Systems — Systemdenken, Trade-offs, Evaluation first, Anti-Hype, messbare Behauptungen, Leserzeit respektieren
Stimme des Reviews: ehrlich, priorisiert, ohne Höflichkeitsfloskeln

───

1. Ein-Satz-Diagnose

Das Buch hat die richtige These und an mehreren Stellen echte Produktionshärte — aber es liest sich oft wie eine Pipeline, die Kapitel stapelt, nicht wie ein Buch, das eine Idee konsequent durchzieht. Die stärksten Kapitel (Prompt, RAG, Evaluation, Agents) tragen den Rest. Die schwächsten (kopierte Autor-Notizen, Scope-Explosion, Tool-Kataloge) untergraben die Glaubwürdigkeit genau der Stimme, die ihr im VOICE_PROFILE anstrebt.

───

2. Was das Buch will — und ob der Aufbau trägt

These (stark)
AI Engineering = deterministische Systeme um probabilistische Modelle: Validierung, Kosten, Latenz, Observability, Security — nicht „Prompts schreiben“.

Das ist der richtige Anker für 2025/26 und näher an AI Engineering als an Prompt-Handbüchern.

TOC in main.tex (sinnvoll)

┌────────────────────────┬────────────────────────────────────────────┬───────────────────────────────────────────────────────┐
│ Teil                   │ Inhalt                                     │ Chip-Urteil                                           │
├────────────────────────┼────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 1 Grundlagen           │ Rolle → Pretrained → Landschaft            │ Richtig. Evaluation fehlt zu früh im Buch.            │
├────────────────────────┼────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 2 Mit dem LLM sprechen │ OpenAI → Tokens → Prompts                  │ OpenAI-zentriert: didaktisch ok, strategisch riskant. │
├────────────────────────┼────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 3 Kontext & Hände      │ RAG → Agents → Multimodal                  │ Stark. Multimodal nach Agents ist ok.                 │
├────────────────────────┼────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 4 Messen & Optimieren  │ Eval → Inference → Cache/Route/Guards → FT │ Eval zu spät (Teil 4 statt Teil 2/3).                 │
├────────────────────────┼────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 5 In die Welt          │ Deploy → MLOps → Security                  │ Deployment-Titel überlappt Observability + Security.  │
└────────────────────────┴────────────────────────────────────────────┴───────────────────────────────────────────────────────┘

Chip-Regel verletzt: Evaluation ist in AI Engineering früh und zentral. Hier lernen Leser RAG und Agents, bevor sie systematisch messen. In Produktion ist das die Reihenfolge, in der Teams scheitern.

Empfohlene TOC-Verschiebung (ohne Inhaltsverlust):

Rolle → Pretrained → Landscape
→ Tokens (Kosten als Constraint)
→ Prompt
→ Evaluation   ← hier rein
→ RAG → Agents → Multimodal
→ Cache/Route/Guards → Inference → Fine-Tuning
→ Deploy → MLOps → Security
→ Checklist

───

3. Gesamtnoten

┌──────────────────────────┬──────┬────────────────────────────────────────────────────────────────────┐
│ Dimension                │ Note │ Kommentar                                                          │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ These / Positionierung   │ A−   │ Klar, abgrenzbar von ML Engineering                                │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Curriculum-Abdeckung     │ A    │ roadmap.sh + Production Layer — vollständig                        │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Systemdenken             │ B+   │ Diagramme und Trade-offs oft gut; Failure Modes ungleichmäßig      │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Evidence / Messrahmen    │ C+   │ Viele Zahlen, zu oft ohne n / Metrik-Definition / Scope            │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Redundanz-Kontrolle      │ D+   │ Gleiche Stories, gleiche Sätze, gleiche „94 %“ quer durchs Buch    │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Kapitel-Kohärenz         │ C    │ 01/06/07 stark; 05/13/15/16 Einstiege oft falsch oder dünn         │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Stimme (Chip-Profil)     │ B    │ Kap. 01/06/07 nahe am Ziel; Rest oft Lehrbuch-Template             │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Craft / LaTeX-Integrität │ C−   │ Kaputte Listings, Label-Kollision, TOC-Teaser falsch               │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Haltbarkeit (timeless)   │ C    │ Policy „keine Jahreszahlen“ vs. Text voller 202x + Model-Snapshots │
├──────────────────────────┼──────┼────────────────────────────────────────────────────────────────────┤
│ Als Gesamtwerk           │ B−   │ Sehr gutes Material; noch kein Buch mit einem Atem                 │
└──────────────────────────┴──────┴────────────────────────────────────────────────────────────────────┘

───

4. Kapitel-für-Kapitel

Skala: A = so lassen / nur polieren · B = gut, straffen · C = umbauen · D = Rewrite-Kandidat · F = broken/trust-breaking

Teil 1 — Grundlagen

Kap. 1 — Was macht ein AI Engineer eigentlich? · B−
Stark: Guards vs. Käfige · Shift Model→Integration · Trade-off-Tabelle · Interview-Fragen · Praxisprojekt mit Injection-Samples.
Schwach: Scope-Explosion (Security, Cache, Routing schon hier) · Glossar-Dump · kaputtes TypeScript (\end{praxishinwisus}) · Teaser sagt „Prompt Engineering“, TOC sagt Pretrained Models · Reality-Check-Überladung (24×).
Chip-Fix: Mental Map + 1 Case + 1 Code + Anti-Patterns. Rest → Vorwärtsverweis.

Kap. 2 — Pre-trained Models · B
Stark: Transfer Learning, Typologie, FT vs. Prompt als Entscheidung.
Schwach: Pre-Training wird zweimal erklärt · Deutsch-Token 1.8× widerspricht Kap. 1 (1.3×) und Kap. 5 (1.4–2×) · Teaser wieder falsch („Prompt Engineering“).
Chip-Fix: Eine saubere Typologie + Entscheidungsbaum „wann trainieren / wann nicht“. Theorie nicht doppeln.

Kap. 3 — Model-Landschaft · B+
Stark: 4-Layer-Stack (LLM / RAG / Agents / MCP) als Map · Multi-Provider-Story · „kein bestes Modell“.
Schwach: Fast keine Reality-Checks · MCP sehr früh und dominant (kann datieren) · Benchmark-Kritik könnte schärfer mit eigenen Eval-Workflows.
Chip-Fix: Provider-Preise als „austauschbare Tabelle“, Prinzipien im Fließtext.

Teil 2 — Mit dem LLM sprechen

Kap. 4 — OpenAI Platform · C+
Stark: API-Mechanik, Rate Limits, Structured Outputs, Streaming — nützlich.
Schwach: Autor-Notiz 1:1 wie Prompt-Kapitel (\$400→\$12, 61 %→94 %) · OpenAI-only als Kern des Buchs veraltet die Marke · wenig Reality-Checks · Anthropic/Google nur Rand.
Chip-Fix: „Chat Completions Contract“ provider-agnostisch; OpenAI als Referenzimplementierung, nicht als Religion.

Kap. 5 — Token-Management und Kosten · C− / D
Stark: Tokenizer, Context Window, Lost-in-the-Middle, Input vs. Output-Pricing — der richtige Kern.
Kritisch: Autor-Notiz ist die RAG-E-Commerce-Story (Hit Rate, Pinecone, Re-Ranker) — falsches Kapitel. Das zerstört Trust im ersten Absatz.
Schwach: Kürzer und dünner als Nachbarn · Semantic Router / Cache schon hier, dann wieder in Kap. 12.
Chip-Fix: Eigene Token-Story mit \$/Query, max_tokens, History-Kompression. RAG-Story raus.

Kap. 6 — Prompt Engineering · A−
Stark: Mechanismen (ICL, Format Following, Attention Bias) · Pyramide · Versionierung · Temperature als Entropie · Anti-Injection an der Schnittstelle · dicht, chip-nah.
Schwach: Kleiner LaTeX-Bruch (end{praxish) · Reality-Check-Dichte hoch · Self-Consistency gut erklärt.
Chip-Fix: Fast so lassen; nur straffen und Messrahmen bei „94 % Accuracy“ nachziehen.

Teil 3 — Kontext & Hände

Kap. 7 — RAG · A−
Stark: Offline/Online-Pipelines · Chunking als Hebel · pgvector-Default mit Begründung · HyDE/Multi-Query/Re-Ranker mit „wann lohnt sich“ · Golden Set für Retrieval · Indirect Injection.
Schwach: Mehrere end{praxish…-Brüche · Fine-Tuning-vs-RAG-Absatz kopiert aus Kap. 2 · Zahlen (67 %→94 %) ohne Dataset-Protokoll.
Chip-Fix: Der stärkste Produktions-Kern des Buchs. Polieren, nicht neu erfinden.

Kap. 8 — AI Agents · B+
Stark: Loop-Denken · Memory · max_steps-Horrorstory (\$400 in 4 Min) · Orchestrierung statt Framework-Hype.
Schwach: 1180 Zeilen — längstes Kapitel · 0 Reality-Checks · Teaser → Evaluation, TOC → Multimodal · Framework-Abschnitte drohen zu datieren.
Chip-Fix: „Agent = constrained loop“ in 60 % Länge; Frameworks in Tabelle mit Haltbarkeitswarnung.

Kap. 14 — Multimodale KI · B−
Stark: Vision/Audio/Token-Äquivalenz von Bildern — oft unterschätzt.
Schwach: Template-Autor-Notiz-Risiko · weniger Mechanismus-Tiefe als Prompt/RAG · im Fluss zwischen Agents und Eval etwas „Side Quest“.
Chip-Fix: An RAG koppeln (Vision-RAG, Doc-Parsing) statt isolierter Feature-Tour.

Teil 4 — Messen & Optimieren

Kap. 9 — Evaluation · A
Stark: Qualität/Kosten/Latenz-Triangle · Golden Sets · LLM-as-Judge-Fallen · CI-Gates · beste Alignment mit Chip.
Schwach: Zu spät im Buch · Autor-Notiz gut, aber „Multi-Judge“ braucht Bias-Diskussion tiefer.
Chip-Fix: Nach vorne ziehen. Dieses Kapitel sollte früher das Leseverhalten prägen.

Kap. 11 — Inference Optimization · B
Stark: Prefill vs. Decode · TTFT/TPOT · vLLM/PagedAttention · Quantisierung „nie blind“ · Beispielrechnung.
Schwach: Englischer Kapiteltitel im deutschen Buch · dünner als RAG · Zielgruppe unklar (API-first Engineers vs. GPU-SRE).
Chip-Fix: Klar trennen: „Du brauchst das nur bei Self-Host / hohem Volume“ + Skip-Box.

Kap. 12 — Caching, Routing, Guardrails · B+
Stark: Drei Cache-Ebenen · Semantic Cache Thresholds · Router-Kosten · Budget-Controller · gute Praxishinweise.
Schwach: Guardrails und Security-Kap. 16 · Caching schon in 01/05/06 · 0 Reality-Checks im Chip-Format.
Chip-Fix: Security-Guards nur als Pipeline-Skizze; Detail → Kap. 16. Cost-Stack hier als eine Story.

Kap. 13 — Model Customization · C
Stark: PEFT/LoRA/QLoRA, Dataset-Qualität, wann FT.
Kritisch: Autor-Notiz wieder die RAG-E-Commerce-Story — im Fine-Tuning-Kapitel absurd.
Schwach: Überschneidung mit Kap. 2 · weniger „I trained this, measured that“.
Chip-Fix: Neue FT-Story (Format/Style, catastrophic forgetting, Eval before/after). RAG-Anekdote löschen.

Teil 5 — Shipping

Kap. 10 — Deployment… · C+
Titel: „Deployment, Observability und Sicherheit“ — kollidiert mit Kap. 15 und 16.
Stark: External deps, Cost, Probabilistik · FastAPI/Docker · Streaming.
Schwach: Observability und Security halb, nicht voll · Label chap:deployment_observability lügt über Scope.
Chip-Fix: Titel → „Deployment-Architekturen und Betriebsmuster“. Observability → 15, Security → 16, nur Verweise.

Kap. 15 — MLOps / Observability · C−
Stark: LLMOps-Lebenszyklus, Prompts-as-Code, Drift.
Kritisch: Dieselbe RAG-Autor-Notiz wie Kap. 7/13/16.
Schwach: ~1.2k Wörter — dünn · Observability war schon in 01/09/10 · wenig konkrete Dashboard-/Alert-Designs.
Chip-Fix: Entweder aufwerten (Traces, SLOs, cost alerts, prompt drift) oder mit Deploy mergen.

Kap. 16 — Security, Governance, Responsible AI · C
Stark: Defense-in-Depth, EU AI Act, OWASP-LLM-Nähe, Supply Chain.
Kritisch: Wieder RAG-Autor-Notiz — null Bezug zu Security.
Schwach: Injection schon in 01/06/07/12 · Governance und Engineering vermischt ohne klare „was baust du vs. was policy’est du“.
Chip-Fix: Eigene Incident-Story (Injection, PII leak, agent spend). Alles Technische aus früheren Kapiteln hier bündeln, dort nur Teaser.

Anhang

Production Checklist · A−
Genau richtig: druckbar, handlungsfähig, Code-Qualitätskennzeichnung ([Production-Ready] vs. didaktisch). Mehr davon im Fließtext referenzieren.

Glossar · B−
Nützlich, aber end{praxish…-Brüche und Risiko, Definitionen zu widersprechen (Token-Faktor Deutsch etc.).

───

5. Querschnittsprobleme (die echten Blocker)

P0 — Trust Breakers

┌───────────────────────────────────────────────────────────┬───────────────────────────────────────┬────────────────────────────────────────────────┐
│ Problem                                                   │ Wo                                    │ Wirkung                                        │
├───────────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────────────────────────┤
│ Kopierte Autor-Notiz (RAG 67 %→94 %, $450→$38)            │ Kap. 5, 7, 13, 15, 16 (und Varianten) │ Persona wirkt generiert, nicht erfahren        │
├───────────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────────────────────────┤
│ Identische OpenAI/Prompt-Story ($400→$12, 61 %→94 %)      │ Kap. 4 + 6                            │ Doppeltes Opening = schwache Editing-Disziplin │
├───────────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────────────────────────┤
│ Broken LaTeX (praxishinwisus, abgeschnittene end{praxish) │ 01, 06, 07, Glossar                   │ Code-Beispiele unbrauchbar / Build-Risiko      │
├───────────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────────────────────────┤
│ Label-Kollision tab:api-kosten                            │ 02 + 05                               │ Cross-Refs können falsch auflösen              │
├───────────────────────────────────────────────────────────┼───────────────────────────────────────┼────────────────────────────────────────────────┤
│ Falsche Kapitel-Teaser                                    │ 01, 02, 08 vs. TOC                    │ Leser verliert Orientierung                    │
└───────────────────────────────────────────────────────────┴───────────────────────────────────────┴────────────────────────────────────────────────┘

P1 — Strukturelle Redundanz

Themen, die 3–6× erklärt werden, ohne klaren „hier die Tiefe“-Ort:

┌────────────────────────────────────┬────────────────────┬────────────────────────────┐
│ Thema                              │ Erscheint in       │ Soll live in               │
├────────────────────────────────────┼────────────────────┼────────────────────────────┤
│ Semantic Cache / Routing           │ 01, 05, 06, 12     │ 12                         │
├────────────────────────────────────┼────────────────────┼────────────────────────────┤
│ Prompt Injection                   │ 01, 06, 07, 12, 16 │ 16 (+ Teaser in 06/07)     │
├────────────────────────────────────┼────────────────────┼────────────────────────────┤
│ Structured Outputs / Temperature 0 │ 01, 04, 06         │ 06 (+ API-Contract in 04)  │
├────────────────────────────────────┼────────────────────┼────────────────────────────┤
│ RAG vs Fine-Tuning                 │ 02, 07, 13         │ 13 (Matrix), 07 (wann RAG) │
├────────────────────────────────────┼────────────────────┼────────────────────────────┤
│ Observability                      │ 01, 09, 10, 15     │ 09 (Qualität) + 15 (Ops)   │
├────────────────────────────────────┼────────────────────┼────────────────────────────┤
│ Kosten/Token                       │ 01, 05, 12         │ 05 + 12                    │
└────────────────────────────────────┴────────────────────┴────────────────────────────┘

Chip-Buch-Technik: First mention = Intuition + Verweis. Deep chapter = Mechanismus + Code + Zahlen.

P2 — Evidence-Hygiene

Wiederkehrende Muster:
• „94 % Accuracy / Hit Rate“ ohne n, Label-Definition, Baseline
• „40–60 % Cost Reduction“ ohne Traffic-Mix und False-Positive-Rate des Caches
• Deutsch-Token-Faktor 1.3 / 1.8 / 1.4–2 — intern inkonsistent

Minimum-Standard für jede Zahl im Buch:

Metrik · n · Zeitraum/Scope · Baseline · was sich geändert hat

P3 — Stimme ungleichmäßig

┌─────────────────────────────────────────────────────────┬────────────────────────────┐
│ Stil                                                    │ Kapitel                    │
├─────────────────────────────────────────────────────────┼────────────────────────────┤
│ Chip-nah (Mechanismen, Reality Checks, harte Defaults)  │ 01, 06, 07                 │
├─────────────────────────────────────────────────────────┼────────────────────────────┤
│ Gutes Lehrbuch, weniger „I measured“                    │ 03, 08, 09, 11, 12         │
├─────────────────────────────────────────────────────────┼────────────────────────────┤
│ Template-Pipeline (Motivation→Grundlagen→Architektur→…) │ 04, 05, 10, 13, 14, 15, 16 │
└─────────────────────────────────────────────────────────┴────────────────────────────┘

VOICE_PROFILE-Checkliste wird in den späteren Kapiteln systematisch untererfüllt (kaum AUTORnotiz-Varianz, kaum skipdeep, keine Messprotokolle).

P4 — OpenAI-Zentrierung vs. Buchversprechen

Titel und Rolle sagen „AI Engineer“. Der API-Kern ist OpenAI. Das ist didaktisch vertretbar, aber:

• Multi-Provider ist in Kap. 3 versprochen, in Kap. 4 kaum eingelöst
• LiteLLM/Gateway erscheint als Tool, nicht als Architektur-Invariante

P5 — Timelessness vs. Snapshots

Agents.md: keine Jahreszahlen. Realität: Dutzende 202x-Referenzen + GPT-4o / Claude 4 / Gemini 2.5 / Llama 4.

Empfehlung: Prinzipien timeless; Model-Namen nur in Tabellen mit „Stand der Ausgabe“-Fußnote.

───

6. Was sehr gut ist (nicht kaputtreden)

1. Richtige Disziplin-Definition — Integration, nicht Training.
2. Prompt-Kapitel mit Mechanismen — Few-Shot als ICL, nicht als Magie.
3. RAG mit Chunking-first — der richtige Hebel, nicht Embedding-Religion.
4. Evaluation-Kapitel — Golden Set + CI + Judge-Fallen.
5. Agent-Horrorstory (Runaway tool loop) — lehrreich, memorable.
6. pgvector-Default mit ehrlicher „wann du Pinecone brauchst“-Grenze.
7. Production Checklist — das Buch braucht mehr solcher „Operator Surfaces“.
8. Interview-Fragen als Hiring-Rubrik (wo vorhanden) — besser als Trivia.
9. Praxisprojekte in fast jedem Kapitel — rare and valuable.
10. Anti-Patterns-Sektionen — oft der wertvollste Teil eines Kapitels.

───

7. Vergleich zu Chip Huyens AI Engineering (inhaltlich)

┌─────────────────────────────────────┬─────────────────────────┬────────────────────┐
│ Chip-Fokus                          │ Euer Buch               │ Gap                │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Foundation models as infrastructure │ Ja (02, 03)             │ ok                 │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Evaluation early                    │ Kap. 9 spät             │ groß               │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ RAG / context construction          │ Stark (07)              │ ok                 │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Agents as systems with constraints  │ Gut (08), zu lang       │ medium             │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Fine-tuning last                    │ Ja, message richtig     │ Autor-Notiz kaputt │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Architecture & platform             │ Verteilt, OpenAI-lastig │ medium             │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Latency/cost as first-class         │ Ja, aber verstreut      │ consolidate        │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Dataset / data quality              │ Dünn außer FT/RAG       │ Lücke              │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Human feedback / product metrics    │ Angedeutet              │ ausbauen           │
├─────────────────────────────────────┼─────────────────────────┼────────────────────┤
│ Honest uncertainty / skip markers   │ Selten                  │ ausbauen           │
└─────────────────────────────────────┴─────────────────────────┴────────────────────┘

───

8. Priorisierte Roadmap (wenn ich das Buch shippen müsste)

Sprint 1 — Integrity (1–2 Tage)
1. Alle kaputten Listings/Env-Tags fixen (01, 06, 07, Glossar)
2. Label-Kollision tab:api-kosten
3. Einzigartige Autor-Notizen pro Kapitel (bes. 05, 13, 15, 16)
4. Kapitel-Teaser an main.tex-Reihenfolge koppeln
5. Deutsch-Token-Faktor auf eine Zahl/Range vereinheitlichen

Sprint 2 — Architecture (1 Woche)
6. Evaluation nach Prompt (vor oder direkt nach RAG — ideal: nach Prompt, vor RAG)
7. Redundanz-Matrix: First mention vs. Deep chapter
8. Kap. 1 und 10 Scope schneiden
9. Kap. 10 umbenennen; Security/Obs aus dem Titel

Sprint 3 — Evidence & Voice (fortlaufend)
10. Top-30 Zahlen mit Messrahmen
11. Reality-Checks in 03/04/08/11/12/13/15 nachziehen oder bewusst reduzieren und Qualität statt Quantität
12. Skip-Boxen für Theorie-Deep-Dives
13. Code-Labels [Production-Ready] / [Didactic] wie in der Checklist im ganzen Buch

Sprint 4 — Differentiation
14. Provider-agnostischer „LLM Client Contract“
15. Ein durchgängiges Buch-Case (ein Produkt von Kap. 1→16) statt 15 isolierter Anekdoten
16. Data-centric Kapitel/Abschnitt: Logging, Feedback, Online eval, dataset growth

───

9. Leser-Journey (ehrlich)

┌───────────────────────────┬──────────────────────────────────────────────────────────────────────────┐
│ Leser                     │ Erfahrung mit dem Buch heute                                             │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Backend-Dev → AI Engineer │ Gut bedient; riskiert Überforderung durch Early-Security/Cache in Kap. 1 │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ ML Engineer → AI Engineer │ FT/Inference ok; braucht klareren „du trainierst weniger“-Faden          │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Tech Lead / Hiring        │ Interview-Fragen und Checklist stark; Redundanz nervt                    │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Chip-Huyen-Leser          │ Denkt: „richtige Haltung, Editing unfinished, Eval zu spät“              │
└───────────────────────────┴──────────────────────────────────────────────────────────────────────────┘

───

10. Gesamturteil

Material-Note: A− — ihr habt genug Substanz für ein gutes AI-Engineering-Lehrbuch im deutschsprachigen Markt.
Buch-Note: B− — es fehlt die harte Editor-Hand: ein Messstandard, ein Ort pro Thema, echte Kapitel-Openings, Evaluation früher, kaputte Stellen raus.

Was ich als Autorin sagen würde:

Stop adding chapters. Start deleting duplicates and owning every number.
The reader doesn’t need another explanation of semantic caching.
They need to trust that when you say “94 %”, you measured something real — once — and pointed every other chapter at that result.

───

Kurz-Scorecard pro Kapitel

┌──────┬────────────────────┬───────────────────────────┐
│ Kap  │ Titel              │ Note                      │
├──────┼────────────────────┼───────────────────────────┤
│ 01   │ Rolle              │ B−                        │
├──────┼────────────────────┼───────────────────────────┤
│ 02   │ Pretrained         │ B                         │
├──────┼────────────────────┼───────────────────────────┤
│ 03   │ Landschaft         │ B+                        │
├──────┼────────────────────┼───────────────────────────┤
│ 04   │ OpenAI API         │ C+                        │
├──────┼────────────────────┼───────────────────────────┤
│ 05   │ Tokens             │ D (falsche Opening-Story) │
├──────┼────────────────────┼───────────────────────────┤
│ 06   │ Prompt             │ A−                        │
├──────┼────────────────────┼───────────────────────────┤
│ 07   │ RAG                │ A−                        │
├──────┼────────────────────┼───────────────────────────┤
│ 08   │ Agents             │ B+                        │
├──────┼────────────────────┼───────────────────────────┤
│ 09   │ Evaluation         │ A                         │
├──────┼────────────────────┼───────────────────────────┤
│ 10   │ Deployment         │ C+                        │
├──────┼────────────────────┼───────────────────────────┤
│ 11   │ Inference          │ B                         │
├──────┼────────────────────┼───────────────────────────┤
│ 12   │ Cache/Route/Guards │ B+                        │
├──────┼────────────────────┼───────────────────────────┤
│ 13   │ Fine-Tuning        │ C (Opening-Story)         │
├──────┼────────────────────┼───────────────────────────┤
│ 14   │ Multimodal         │ B−                        │
├──────┼────────────────────┼───────────────────────────┤
│ 15   │ MLOps              │ C−                        │
├──────┼────────────────────┼───────────────────────────┤
│ 16   │ Security/Gov       │ C                         │
├──────┼────────────────────┼───────────────────────────┤
│ App  │ Checklist          │ A−                        │
├──────┼────────────────────┼───────────────────────────┤
│ Glos │ Glossar            │ B−                        │
└──────┴────────────────────┴───────────────────────────┘

───

Wenn du als Nächstes willst, kann ich daraus (a) ein konkretes Rewrite-Ticketboard pro Kapitel mit „schneiden / verschieben / neu schreiben“, (b) nur die P0-Integrity-Fixes im Repo umsetzen, oder (c) einen Vorschlag für den durchgängigen Buch-Case (ein Produkt, 16 Kapitel lang).