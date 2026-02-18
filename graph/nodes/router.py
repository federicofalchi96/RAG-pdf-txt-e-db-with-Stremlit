from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from graph.state import GraphState
load_dotenv()

class RouteQuery(BaseModel):
    """Router per indirizzare la domanda alla fonte corretta"""
    choice :Literal["pdf", "DB", "websearch"] = Field(
        description="Scegli la fonte più rilevante: 'pdf', 'DB' o 'websearch' "
    )

llm = ChatOpenAI(model="gpt-4o-mini")
structured_llm = llm.with_structured_output(RouteQuery)

system = """ Sei un router esperto. Data la domanda dell'utente, decidi la fonte più appropriata:

        - pdf: per domande su dettagli specifici dei tuoi 3 PDF locali su LangGraph (es. StateGraph, nodi, edges, checkpointing, ecc.)
        - DB: per definizioni personali, glossario interno o conoscenze fisse che hai memorizzato
        - websearch: per informazioni aggiornate, novità, esempi recenti, o tutto ciò che non è nei tuoi PDF o DB

        Rispondi ESCLUSIVAMENTE con una delle tre opzioni.
        """
router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}")
    ]
)

question_router_chain = router_prompt | structured_llm

def route_question(state: GraphState):
    question = state["question"]
    result: RouteQuery = question_router_chain.invoke({"question": question})
    return {"route": result.choice}