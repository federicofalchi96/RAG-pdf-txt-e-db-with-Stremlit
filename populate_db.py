from database import add_definition

if __name__ == "__main__":
    
    add_definition(
        term="LangGraph",
        definition="""
    LangGraph è una libreria costruita sopra LangChain che permette di creare applicazioni LLM complesse e stateful modellandole come grafi diretti.
    A differenza delle normali chain lineari di LangChain, LangGraph introduce nodi (funzioni), archi (normali e condizionali), stato persistente condiviso tra i nodi e checkpointing automatico.
    È particolarmente potente per agenti con tool calling ciclici, workflow con approvazione umana (Human-in-the-Loop), multi-agent collaboration e applicazioni che richiedono memoria a lungo termine o capacità di "tornare indietro" nello stato.
        """,
        source="LangChain Documentation + Grok",
        category="LangGraph"
    )

    add_definition(
        term="StateGraph",
        definition="""
    StateGraph è la classe principale di LangGraph usata per definire il grafo. Richiede uno schema di stato (tipicamente un TypedDict) e permette di aggiungere nodi con .add_node(), archi fissi con .add_edge() e archi condizionali con .add_conditional_edges().
    Alla fine si compila con .compile() ottenendo un oggetto Runnable che può essere eseguito con .invoke() o .stream(), e supporta checkpointing tramite un checkpointer (es. MemorySaver o PostgresSaver).
        """,
        source="LangGraph Official Examples",
        category="LangGraph"
    )

    add_definition(
        term="add_messages",
        definition="""
    add_messages è un reducer speciale di LangGraph che viene usato come annotazione per il campo messages nello state (es. Annotated[list[AnyMessage], add_messages]).
    Il suo scopo è accumulare i nuovi messaggi nella lista esistente invece di sovrascriverla ad ogni nodo. Senza questo reducer, ogni nodo che restituisce messaggi cancellerebbe la storia precedente della conversazione, rendendo impossibile costruire chatbot o agenti stateful.
    Gestisce automaticamente update (stesso message_id) e rimozione (con RemoveMessage).
        """,
        source="LangGraph Source Code + Documentation",
        category="LangGraph"
    )

    add_definition(
        term="Human-in-the-Loop (HITL)",
        definition="""
    Human-in-the-Loop indica l'integrazione di un intervento umano all'interno di un flusso automatico basato su AI.
    In LangGraph si implementa tipicamente con interrupt_before o interrupt_after su nodi critici (es. prima di indicizzare documenti, prima di generare la risposta finale, o prima di chiamare un tool pericoloso).
    Durante l'interrupt il grafo si ferma, salva lo stato con il checkpointer, e aspetta che l'utente (tramite UI o console) approvi, modifichi o rifiuti. Una volta ripreso, il flusso continua dallo stato salvato.
    È fondamentale per applicazioni enterprise, compliance normativa e riduzione di rischi.
        """,
        source="LangGraph Tutorials + Best Practices 2025",
        category="LangGraph"
    )

    add_definition(
        term="Chroma (vectorstore)",
        definition="""
    Chroma è un database vettoriale open-source, leggero e progettato specificamente per applicazioni AI/LangChain.
    Supporta persistenza locale (cartella con file SQLite), modalità server, e integrazione cloud. In LangChain si usa tramite langchain-chroma e permette di salvare embeddings di documenti, fare similarity search, MMR, e filtraggio metadata.
    La persistenza locale crea una cartella (es. chroma_db/) con un file chroma.sqlite3 che può essere aperto con qualsiasi client SQLite (DBeaver, sqlite-web, DB Browser for SQLite).
    È ideale per prototipi e applicazioni locali/private.
        """,
        source="Chroma Documentation + LangChain Integration",
        category="Vectorstore"
    )

    add_definition(
        term="Retrieval-Augmented Generation (RAG)",
        definition="""
    RAG è un'architettura che combina un retriever (tipicamente un vectorstore) con un LLM generativo.
    Il flusso tipico è: l'utente fa una domanda → il retriever recupera i k chunk più rilevanti dal corpus indicizzato → questi chunk vengono inseriti nel prompt dell'LLM come contesto → l'LLM genera una risposta grounded sui documenti recuperati invece di hallucinare.
    Varianti avanzate includono: HyDE, multi-query retrieval, reranking, compression del contesto, self-query, e integrazione con grafi di conoscenza.
    Obiettivo principale: migliorare accuratezza, attualità e tracciabilità delle risposte LLM.
        """,
        source="Lewis et al. (2020) + Modern Implementations",
        category="RAG"
    )

    add_definition(
        term="Checkpointing in LangGraph",
        definition="""
    Il checkpointing è la capacità di LangGraph di salvare automaticamente lo stato del grafo dopo ogni nodo eseguito.
    Utilizza un checkpointer (es. MemorySaver per sviluppo, PostgresSaver o RedisSaver per produzione) per persistere stato, messaggi, e metadati.
    Permette: ripresa dopo interrupt HITL, time-travel (tornare a stati precedenti), branching (esplorare percorsi alternativi), e persistenza tra sessioni diverse.
    È ciò che rende LangGraph adatto a conversazioni lunghe e workflow complessi.
        """,
        source="LangGraph Documentation",
        category="LangGraph"
    )

    add_definition(
        term="Tavily Search",
        definition="""
    Tavily è un'API di ricerca ottimizzata per agenti LLM e applicazioni RAG.
    A differenza di un normale motore di ricerca, restituisce risultati puliti, con snippet rilevanti, ranking AI-driven e senza pubblicità o clutter.
    Ideale come fallback quando il knowledge base locale non contiene informazioni aggiornate o sufficienti.
    In LangChain si integra come tool (TavilySearchResults) e può essere usato in nodi di fallback o routing condizionale.
        """,
        source="Tavily Documentation",
        category="Tool"
    )