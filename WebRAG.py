import os
import bs4
import shutil
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

if os.path.exists('./chroma_rag_db'):
    shutil.rmtree('./chroma_rag_db')

page_url = "https://blog.csdn.net/2401_88440984/article/details/147496729"
bs4_strainer= bs4.SoupStrainer()

loader = WebBaseLoader(
    web_path=(page_url,),
    bs_kwargs={"parse_only":bs4_strainer}
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

embedding = OllamaEmbeddings(model="nomic-embed-text")

vector_store=Chroma(
    collection_name="rag_collection",
    embedding_function=embedding,
    persist_directory="./chroma_rag_db"
)
ids = vector_store.add_documents(documents=all_splits)