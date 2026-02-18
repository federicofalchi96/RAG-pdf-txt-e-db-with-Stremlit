# ingestion.py
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os

BASE_DIR = Path(__file__).parent
PDF_DIR = BASE_DIR / "pdf"
TXT_DIR = BASE_DIR / "txt"
CHROMA_DIR = BASE_DIR / "chroma.db"

PDF_FILES = [
    "TutorialsuRAGconLangChaineLangGraph_SharedGrokConversation.pdf",
    "LangGraph_AsincronicitàePromptTemplate-Grok.pdf",
    "HITLLangGraph_TutorialedEsempi_SharedGrokConversation.pdf"
]
TXT_FILE = "file1.txt"

if os.path.exists(CHROMA_DIR):
    print("Vectorstore già esistente in ./chroma.db")
    print("Puoi eseguire direttamente python main.py")
    exit()

print("Caricamento e indicizzazione documenti...")

documents = []

for pdf_name in PDF_FILES:
    pdf_path = PDF_DIR / pdf_name
    if pdf_path.exists():
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())
        print(f"Caricato {pdf_name}")
    else:
        print(f"PDF non trovato: {pdf_name}")

txt_path = TXT_DIR / TXT_FILE
if txt_path.exists():
    loader = TextLoader(str(txt_path), encoding="utf-8")
    documents.extend(loader.load())
    print(f"Caricato {TXT_FILE}")

if not documents:
    raise ValueError("Nessun documento caricato. Controlla le cartelle pdf/ e txt/")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Creati {len(chunks)} chunk")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)

print(f"\nVectorstore creato e salvato in {CHROMA_DIR}")
print("Ora puoi eseguire: python main.py")