from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from graph.state import GraphState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Sei un assistente esperto in LangGraph e RAG.
        Rispondi in italiano, in modo chiaro, conciso e tecnicamente accurato.

        Usa principalmente le informazioni dal contesto fornito.
        Se il contesto è utile, citane le fonti ([Locale X] o [Web X]).
        Se non hai informazioni sufficienti o il contesto è ambiguo, puoi:
        - Dire "Non ho informazioni sufficienti nei documenti locali o nella ricerca web"
        - OPPURE integrare conoscenze generali se strettamente necessarie, ma segnalalo con [Conoscenza generale]

        Contesto recuperato:
        {context}
    """ ),
    ("human", "{question}")
])

def format_context(state: GraphState) -> str:
    parts = []
    if state.get("documents"):
        for i, doc in enumerate(state["documents"], 1):
            parts.append(f"[Locale {i}] {doc.page_content[:500]}")
    if state.get("web_results"):
        for i, result in enumerate(state["web_results"], 1):
            parts.append(f"[Web {i}] {result}")
    context_str = "\n\n".join(parts) if parts else "Nessun contesto recuperato."
    return context_str

def generate_response(state: GraphState)-> dict:
    context = format_context(state)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"question": state["question"], "context": context})
    return {"generated_response": response}