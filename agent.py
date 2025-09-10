import os
import re
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Paths
DOCS_PATH = "docs"          
VECTORSTORE_PATH = "vectorstore"

# Initialize embeddings and model
embeddings = OllamaEmbeddings(model="llama3.2")
llm = Ollama(model="llama3.2")

# Load all documents from docs/
def load_documents():
    docs = []
    for file in os.listdir(DOCS_PATH):
        path = os.path.join(DOCS_PATH, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())

    if not docs:
        raise FileNotFoundError(f"No source documents found in '{DOCS_PATH}' to build FAISS index.")
    
    return docs

# Load or create FAISS index
def get_vectorstore():
    persist_dir = VECTORSTORE_PATH

    if os.path.exists(os.path.join(persist_dir, "index.faiss")):
        return FAISS.load_local(
            persist_dir,
            embeddings,
            allow_dangerous_deserialization=True
        )
    
    docs = load_documents()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(persist_dir)
    return db

# Load vectorstore
db = get_vectorstore()

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
)

# Parse LLM response for brand name and slogan
def parse_llm_response(response: str):
    name_match = re.search(r"\*\*Brand Name:\*\*\s*(.+)", response)
    slogan_match = re.search(r"\*\*Slogan:\*\*\s*(.+)", response)
    name = name_match.group(1).strip() if name_match else "Name not generated"
    slogan = slogan_match.group(1).strip() if slogan_match else "Slogan not generated"
    return name, slogan

# Generate branding
def generate_branding(description: str):
    # Retrieve relevant docs (just top k summaries)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(description)
    context = "\n".join([d.page_content for d in docs])

    # LLM prompt
    prompt = f"""
You are a branding expert. Based on the description below and the provided references, create UNIQUE outputs.
Do NOT copy text from the documents. Be creative and imaginative.

User description:
{description}

Reference keywords or insights:
{context}

Please generate in this format:
**Brand Name:** <creative brand name>
**Slogan:** <short impactful slogan>
"""
    response = llm.invoke(prompt)
    print("LLM Response:", response)  # para debug

    name, slogan = parse_llm_response(response)

    return {
        "name": name,
        "slogan": slogan,
        "context": context
    }