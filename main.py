from dotenv import load_dotenv
load_dotenv()

import uuid
import streamlit as st
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from graph.state import GraphState
from graph.nodes.router import route_question
from graph.nodes.retrieve import retrieve_pdf, retrieve_db, retrieve_web
from graph.nodes.grade_docs import grade_documents
from graph.nodes.generate import generate_response
from graph.graph import app


thread_id = str(uuid.uuid4())
config = {"configurable" : {"thread_id" : thread_id}}

question = input("\n Fammi una domanda su langgraph: ")
if not question:
    print("Domanda vuota. Esci.")
    exit()

print("\n Elaborazione in corso.\n")

for step in app.stream({"question": question}, config, stream_mode="values"):
    if step.get("generated_response"):
        print("Bozza di risposta:\n")
        print(step["generated_response"])

#HITL

decision = input("\n\nApprovi questa risposta? (approved / not_approved): ").strip().lower()

if decision == "approved":
    app.update_state(config, None, as_node="approve")
    print("Risposta approvata!")
else:
    print("\n Rifiutata. Ricerca sul web in corso...")
    app.update_state(config, None, as_node="retrieve_web")

for step in app.stream(None, config, stream_mode="values"):
    if step.get("generated_response"):
        print("\n RISPOSTA FINALE:\n")
        print(step["generated_response"])

print("\nFine.")