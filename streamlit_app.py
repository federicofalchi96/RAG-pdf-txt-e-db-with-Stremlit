from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from graph.graph import app
import uuid

st.set_page_config(page_title="RAG LangGraph Chatbot", layout="wide")
st.title("Agente RAG su LangGraph con Approvazione Umana")
st.markdown("Fai domande su LangGraph")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "waiting_approval" not in st.session_state:
    st.session_state.waiting_approval = False
if "current_draft" not in st.session_state:
    st.session_state.current_draft = None

query = st.text("Benvenuto utente! Cosa vuoi chiedermi? ")
config = {"configurable" : {"thread_id" : st.session_state.thread_id}}


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query := st.chat_input("Fammi una domanda su Langgraph:"):
    st.session_state.messages.append({"role":"user", "content":query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Elaborazione in corso..."):
        draft = ""
        placeholder = st.empty()

        for event in app.stream({"question" : query}, config, stream_mode="values"):
            if event.get("generated_response"):
                draft = event["generated_response"]
                st.session_state.current_draft = draft

        placeholder.markdown(draft)

        st.session_state.waiting_approval = True

if st.session_state.waiting_approval:
    st.markdown("Approvi questa bozza? ")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Approva", use_container_width=True):
            app.update_state(config, None, as_node="approve")
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_draft})
            st.session_state.waiting_approval = False
            st.success("Risposta **approvata** e salvata nella chat")
            st.rerun()
    with col2:
        if st.button("Rifiuta e ricerca nel web", use_container_width=True):
            with st.spinner("Ricerca web in corso e rigenerazione risposta"):
                app.update_state(config, {"generated_response": None,
                                          "needs_web": False,
                                          "documents" : None},
                                          as_node = "retrieve_web")
                
                state_after_web = app.get_state(config).values
                st.write("DEBUG dopo retrieve_web:")
                st.json({
                    "web_results": state_after_web.get("web_results"),
                    "documents": state_after_web.get("documents"),
                    "needs_web": state_after_web.get("needs_web")
                })

                new_draft = ""
                placeholder = st.empty()

                for event in app.stream(None, config, stream_mode="values"):
                    if event.get("generated_response"):
                        new_draft = event["generated_response"]
                        placeholder.markdown(new_draft + "▌")

                placeholder.markdown(new_draft)

                st.session_state.messages.append({"role": "assistant", "content": new_draft})
                st.session_state.waiting_approval = False
                st.success("Risposta rigenerata con fonti web!")
                st.rerun()

if st.button("Nuova conversazione"):
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.waiting_approval = False
    st.session_state.current_draft = None
    config["configurable"]["thread_id"] = st.session_state.thread_id
    st.rerun()


