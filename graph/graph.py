from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.nodes.router import route_question
from graph.nodes.retrieve import retrieve_pdf, retrieve_db, retrieve_web
from graph.nodes.grade_docs import grade_documents
from graph.nodes.generate import generate_response
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()


def route_after_grading(state: GraphState)-> str:
    return "retrieve_web" if state.get("needs_web", False) else "generate"

workflow = StateGraph(GraphState)

workflow.add_node("route", route_question)
workflow.add_node("retrieve_pdf", retrieve_pdf)
workflow.add_node("retrieve_db", retrieve_db)
workflow.add_node("retrieve_web", retrieve_web)
workflow.add_node("grade_docs", grade_documents)
workflow.add_node("generate", generate_response)
workflow.add_node("approve", lambda s:s)
workflow.add_edge(START, "route")
workflow.add_conditional_edges(
    "route",
    lambda state: state["route"],
    {
        "pdf":"retrieve_pdf",
        "DB":"retrieve_db",
        "websearch":"retrieve_web"
    }
)
workflow.add_edge("retrieve_pdf", "grade_docs")
workflow.add_edge("retrieve_db", "grade_docs")
workflow.add_edge("retrieve_web", "generate")

workflow.add_conditional_edges(
    "grade_docs",
    route_after_grading,
    {
        "generate": "generate",
        "retrieve_web":"retrieve_web"
    }
)

workflow.add_edge("generate", "approve")
workflow.add_edge("approve", END)

app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["approve"]
)

    #                                +-----------------+
    #                                |     START       |
    #                                +-----------------+
    #                                           |
    #                                           v
    #                                +-----------------+
    #                                |     route       |  ← Decide fonte: "pdf", "DB" o "websearch"
    #                                +-----------------+
    #                                           |
    #               +---------------------------+---------------------------+
    #               |                           |                           |
    #               v                           v                           v
    #   +-------------------+       +-------------------+       +-------------------+
    #   |  retrieve_pdf     |       |  retrieve_db      |       |  retrieve_web     |
    #   | (Chroma locale)   |       | (Chroma locale)   |       | (Tavily search)   |
    #   +-------------------+       +-------------------+       +-------------------+
    #               |                           |                           |
    #               +-------------+-------------+                           |
    #                             |                                         |
    #                             v                                         |
    #                    +-----------------+                                |
    #                    |   grade_docs    |  ← Valuta se docs locali sono |
    #                    |                 |     rilevanti; se no, web     |
    #                    +-----------------+                                |
    #                             |                                         |
    #               +-------------+-------------+                           |
    #               |                           |                           |
    #               v                           v                           |
    #           (buoni docs)               (docs insufficienti)            |
    #               |                           |                           |
    #               +-------------+-------------+                           |
    #                             |                                         |
    #                             v                                         v
    #                    +-----------------+                       +-----------------+
    #                    |    generate     |                       |  retrieve_web   |
    #                    | (risposta bozza)|  ← Genera con fonti     +-----------------+
    #                    +-----------------+    citate                        |
    #                             |                                            |
    #                             +-----------------+--------------------------+
    #                                               |
    #                                               v
    #                                      +-----------------+
    #                                      |     approve     |  ← Dummy per HITL
    #                                      +-----------------+
    #                                               |
    #                                     INTERRUPT BEFORE "approve"
    #                                     (pausa per input umano)
    #                                               |
    #                             +-----------------+-----------------+
    #                             |                                   |
    #                             v                                   v
    #                       APPROVED                            NOT APPROVED
    #                             |                                   |
    #                             v                                   v
    #                        +-------+                        +-----------------+
    #                        |  END  |                        |  Torna al nodo  |
    #                        +-------+                        |  "route" o      |
    #                                                         |  direttamente a  |
    #                                                         |  "retrieve_web"  |
    #                                                         +-----------------+