# 02 vorgefertigte modelle – Block 2

## Beschreibung

Das Resultat sind Modelle wie GPT-4o, Claude, Gemini oder Llama -- sie alle wurden auf diese Weise vortrainiert. Die eigentliche Kunst liegt dann im \textbf{Fine-Tuning} und der \textbf{Integration} dieser Foundation Models in Anwendungslogik.

## Verbatim

```
Phase 1: Pre-Training
+--------------------+     +------------------+
|  Internet-Korpus   | --> |  Next-Token-      |
|  (Petabytes Text)  |     |  Prediction       |
+--------------------+     +--------+---------+
                                    |
                          +---------v----------+
                          |  Foundation Model   |
                          |  (roh, generalisiert)|
                          +---------+----------+
                                    |
               +--------------------+--------------------+
               |                    |                    |
     Phase 2a: Fine-Tuning   Phase 2b: Prompt-Tuning  Phase 2c: RAG
               |                    |                    |
     +---------v---------+  +------v-------+   +-------v--------+
     | Domänen-spezifisch |  | In-Context   |   | Externes Wissen |
     | (Recht, Medizin)   |  | Learning     |   | (Dokumente, DB) |
     +-------------------+  +--------------+   +----------------+
               |                    |                    |
               +--------------------+--------------------+
                                    |
                          +---------v----------+
                          |  Production-LLM     |
                          |  (angepasst)        |
                          +--------------------+
```
