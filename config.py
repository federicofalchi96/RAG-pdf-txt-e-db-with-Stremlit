from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_tavily import TavilySearch
from pathlib import Path

BASE_PATH = Path(__file__).parent
CHROMA_PATH = BASE_PATH / "chroma.db"

embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")
llm = ChatOpenAI(model= "gpt-4o-mini", temperature=0)

vectorstore = Chroma(persist_directory=str(CHROMA_PATH), embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k":4})

tavily = TavilySearch(max_result=3)