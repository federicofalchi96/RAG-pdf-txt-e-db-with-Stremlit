# RAG Agent con LangGraph + Human-in-the-Loop

Un agente RAG intelligente che:
- Usa 3 PDF locali + glossario personale (vectorstore Chroma)
- Fa routing intelligente (locale vs web)
- Grading documenti + fallback su Tavily se insufficienti
- Human-in-the-Loop: approva/rifiuta bozza
- Citazione fonti [Locale X] / [Web X]

## Struttura

- `graph/` → logica LangGraph (stato, nodi, grafo)
- `ingestion.py` → crea il vectorstore Chroma
- `app.py` → interfaccia Streamlit
- `pdf/` e `txt/` → documenti sorgente

## Installazione

1. Clona la repo
   ```bash
   git clone https://github.com/tuo-username/rag-langgraph.git
   cd rag-langgraph

2. Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Installa dipendenze
Installa dipendenzeBashpip install -r requirements.txt

4. Crea .env

5. Indicizza i documenti una sola volta
python ingestion.py

6. Avvia l'app

streamlit run streamlit_app.py

Funzionalità principali

Router intelligente (locale vs web)
Retrieval da Chroma (PDF + glossario)
Ricerca Tavily su rifiuto umano
HITL con approvazione/rifiuto
Citazione fonti automatica
