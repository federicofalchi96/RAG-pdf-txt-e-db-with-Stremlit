from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from graph.state import GraphState
from typing import Literal

class RelevanceGrade(BaseModel):
    source :Literal["yes","no"] = Field(description=" 'yes' se i documenti sono rilevanti, 'no' altrimenti")

llm = ChatOpenAI(model="gpt-4o-mini")
structured_llm = llm.with_structured_output(RelevanceGrade)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Valuta se i documenti forniti sono rilevanti per rispondere alla domanda. Rispondi solo 'yes' o 'no'."),
        ("human", "Domanda: {question} \n\n Documenti: \n {context}")                
    ]
)

chain = prompt | structured_llm

def grade_documents(state: GraphState)->dict:
    if not state.get("documents"):
        return {"needs_web": True}
    
    context = "\n\n".join([doc.page_content for doc in state["documents"]])
    result = chain.invoke({"question": state["question"], "context": context})
    return {"needs_web": result.source == "no"}