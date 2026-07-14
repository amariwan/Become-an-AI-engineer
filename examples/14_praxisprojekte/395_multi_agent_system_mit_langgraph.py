# Multi-Agent-System mit LangGraph
# Quelle: chapters/14_praxisprojekte.tex (Zeile 395)
from langgraph.graph import StateGraph, MessagesState, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list[dict]
    research_done: bool
    analysis_ready: bool

def researcher_node(state: AgentState) -> AgentState:
    """Agent 1: Recherchiert in der Wissensdatenbank."""
    last_msg = state["messages"][-1]["content"]
    research_results = search_knowledgebase(last_msg)
    return {
        "messages": [{"role": "assistant",
                      "content": f"[Forschungsergebnis]\n{research_results}"}],
        "research_done": True,
    }

def analyst_node(state: AgentState) -> AgentState:
    """Agent 2: Analysiert die Recherche-Ergebnisse."""
    research_text = "\n".join(
        m["content"] for m in state["messages"]
        if "[Forschungsergebnis]" in m.get("content", "")
    )
    analysis = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user",
                   "content": f"Analysiere:\n\n{research_text}"}]
    )
    return {
        "messages": [{"role": "assistant",
                      "content": f"[Analyse]\n{analysis.choices[0].message.content}"}],
        "analysis_ready": True,
    }

def writer_node(state: AgentState) -> AgentState:
    """Agent 3: Schreibt den finalen Bericht."""
    all_content = "\n".join(m["content"] for m in state["messages"])
    final_report = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user",
                   "content": f"Schreibe Bericht basierend auf:\n\n{all_content}"}]
    )
    return {
        "messages": [{"role": "assistant",
                      "content": final_report.choices[0].message.content}],
    }

workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("writer", writer_node)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()
result = app.invoke({
    "messages": [{"role": "user",
                  "content": "Analysiere die neuesten KI-Trends."}],
})

