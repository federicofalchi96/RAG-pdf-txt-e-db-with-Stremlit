from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from graph.state import GraphState
from pathlib import Path
import os

# Percorso assoluto e coerente
BASE_DIR = Path(__file__).parent.parent.parent
CHROMA_DIR = BASE_DIR / "chroma.db"
vectorstore = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=OpenAIEmbeddings())
local_retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

tavily = TavilySearchResults(max_results=3)

def retrieve_local(state: GraphState):
    print("Retrieval documenti locali (PDF e Glossario)")
    docs = local_retriever.invoke(state["question"])
    return {"documents" : docs}

def retrieve_web(state:GraphState):
    print("Ricerca tavily")
    try:
        results = tavily.invoke(state["question"])
        web_results = []
        for r in results:
            title = r.get("title", "Senza titolo")
            url = r.get("url", "URL non disponibile")
            content = r.get("content") or r.get("raw_content") or ""
            content = content[:2000] + "..." if len(content) > 2000 else content
            web_results.append(f"**Titolo:** {title}\n**Fonte:** {url}\n**Contenuto:** {content}")
        
        print("DEBUG: web_results trovati:", len(web_results))  # log
        return {"web_results": web_results or ["Nessun risultato utile da Tavily"]}
    except Exception as e:
        print("ERRORE Tavily:", e)
        return {"web_results": [f"Errore ricerca web: {str(e)}"]}

retrieve_pdf = retrieve_local
retrieve_db = retrieve_local
