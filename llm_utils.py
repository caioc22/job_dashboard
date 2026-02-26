import os
import requests
import subprocess
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd



def get_windows_ip():
    cmd = "ip route show | grep default | awk '{print $3}'"
    return subprocess.check_output(cmd, shell=True).decode().strip()


BASE_URL = f"http://{get_windows_ip()}:11434"
VECTOR_DB_PATH = "./chroma_db"


def process_text_local_ollama_server(text, prompt="Summarize:", model="qwen3:8b"):
    url = f"{BASE_URL}/"
    response = requests.get(url, timeout=3)
    print(response)

    url = f"{BASE_URL}/api/generate"
    print(f"Trying windows connection: {url}")

    payload = {
        "model": model,
        "prompt": f"{prompt}\n\n{text}",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        print(f"Erro: {e}")
        return None


def check_available_models():

    try:
        response = requests.get(f"{BASE_URL}/api/tags", timeout=5)
        models = response.json().get("models", [])
        if not models:
            raise RuntimeError("No models available on Ollama server.")
        
        return [m['name'] for m in models]
    
    except Exception as e:
        raise RuntimeError(f"Could not fetch models from Ollama: {e}")


class RAG:
    _instance = None
    _retriever = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_chain(self):
        if self._retriever is None:
            self._retriever = self._initialize_chain()
        return self._retriever

    def _initialize_chain(self):
        
        models = check_available_models()
        print(models)
        
        embed = None; model = None
        if "qwen3.8b" in models:
            model = "qwen3.8b"
        else:
            for m in models:
                if "embed" in m:
                    if not embed:
                        embed = m
                else:
                    if not model:
                        model = m
            
        print(embed, model)

        llm = ChatOllama(model=model, base_url=BASE_URL, temperature=0)
        
        # if not os.path.exists(VECTOR_DB_PATH):
        # print("Initializing Chroma vector database...")
        embeddings = OllamaEmbeddings(model=embed, base_url=BASE_URL)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        data = pd.read_csv("jobs.csv")["description"].tolist()
        filtered_data = [str(d) for d in data if isinstance(d, str) and d.strip()]

        docs = text_splitter.create_documents(filtered_data)

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=VECTOR_DB_PATH
        )

        prompt_template = ChatPromptTemplate(
            input_variables=["context", "input"],
            messages=[
                ("system", """
                    You are a job market analyst assistant. 
                    You help users extract insights from job vacancy descriptions, such as required skills, experience levels, technologies, and salary ranges.
                    Answer based only on the job vacancies provided below. If the answer is not found in the vacancies, say you don't know.
                    Vacancies:
                    {context}"""
                 ),
                ("human", "{input}")
            ]
        )

        document_chain = create_stuff_documents_chain(llm, prompt_template)
        
        return create_retrieval_chain(
            vectorstore.as_retriever(search_kwargs={"k": 2}),
            document_chain
        )
    

    def query(self, question):
        retriever = self.get_chain()
        result = retriever.invoke({"input": question})
        return result["answer"]