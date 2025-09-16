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
    index_path = os.path.join(persist_dir, "index.faiss")

    # se já existe um índice salvo
    if os.path.exists(index_path):
        index_mtime = os.path.getmtime(index_path)  # última modificação do índice

        # pega a última modificação entre os docs
        docs_mtime = max(
            os.path.getmtime(os.path.join(DOCS_PATH, f))
            for f in os.listdir(DOCS_PATH)
        )

        # se os docs foram atualizados depois do índice -> rebuild
        if docs_mtime > index_mtime:
            print("📌 Detectamos atualização nos docs → reconstruindo FAISS...")
            docs = load_documents()
            db = FAISS.from_documents(docs, embeddings)
            db.save_local(persist_dir)
            return db
        else:
            print("✅ Usando FAISS em cache (nenhuma atualização nos docs).")
            return FAISS.load_local(
                persist_dir,
                embeddings,
                allow_dangerous_deserialization=True
            )
    else:
        print("📌 Nenhum índice encontrado → criando FAISS novo...")
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

# Parse LLM response for brand name, slogan, and concept
def parse_llm_response(response: str):
    # Primeiro tenta pelo formato esperado (com **)
    name_match = re.search(r"\*\*Brand Name:\*\*\s*(.+)", response)
    slogan_match = re.search(r"\*\*Slogan:\*\*\s*(.+)", response)
    logo_mark = re.search(r"\*\*Logo Mark:\*\*\s*(.+)", response)
    color = re.search(r"\*\*Color:\*\*\s*(.+)", response)
    concept_match = re.search(r"\*\*Branding Concept:\*\*\s*(.+)", response, re.DOTALL)

    # Se não achar, tenta pegar versões mais soltas
    if not name_match:
        name_match = re.search(r"(?i)(?:Brand Name|Name)[:\-]?\s*([^\n]+)", response)

    if not slogan_match:
        slogan_match = re.search(r"(?i)(?:Slogan)[:\-]?\s*([^\n]+)", response)

    if not logo_mark:
        logo_mark = re.search(r"(?i)(?:Logo Mark)[:\-]?\s*(.+)", response, re.DOTALL)
    
    if not color:
        color = re.search(r"(?i)(?:Color)[:\-]?\s*(.+)", response, re.DOTALL)

    if not concept_match:
        concept_match = re.search(r"(?i)(?:Branding Concept)[:\-]?\s*(.+)", response, re.DOTALL)

    name = name_match.group(1).strip() if name_match else "Name not generated"
    slogan = slogan_match.group(1).strip() if slogan_match else "Slogan not generated"
    logo_mark = logo_mark.group(1).strip() if logo_mark else "Logo Mark not generated"
    color = color.group(1).strip() if color else "Logo Mark not generated"
    concept = concept_match.group(1).strip() if concept_match else "Concept not generated"

    return name, slogan, concept, logo_mark, color

# Generate branding
def generate_branding(description: str):
    # Retrieve relevant docs (just top k summaries)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(description)
    context = "\n".join([d.page_content for d in docs])
    print("context:\n", context)

    # LLM prompt
    prompt = f"""
You are a branding expert. Based on the description below and the provided references, create ONE SINGLE branding suggestion.

⚠️ Important:
- Return ONLY ONE brand name, ONE slogan, and ONE short branding concept.
- Do NOT generate multiple options.
- Choice one of these colors: 
    green, mint, bright, spring, aqua, soft, summer, coastal, cream, warm, pink, blue, earthy, neutral, elegant, vibrant
- Follow this exact format:

**Brand Name:** <creative brand name>  
**Slogan:** <short impactful slogan>
**Logo Mark: <basic logo mark>**
**Color:** <green, mint, bright, spring, aqua, soft, summer, coastal, cream, warm, pink, blue, earthy, neutral, elegant OR vibrant>
**Branding Concept:** <short explanation>

User description:
{description}

Reference keywords or insights:
{context}
"""
    response = llm.invoke(prompt)
    print("LLM Response:", response)

    name, slogan, concept, logo, color = parse_llm_response(response)

    return {
        "name": name,
        "slogan": slogan,
        "logo_mark": logo,
        "color": color,
        "explanation": concept
    }