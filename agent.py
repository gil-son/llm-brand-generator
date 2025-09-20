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


def load_documents():
    """
    Load all documents from the docs/ folder.
    Supports both PDF and TXT files.

    Returns:
        list: A list of loaded documents.
    Raises:
        FileNotFoundError: If no documents are found in the folder.
    """
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


def get_vectorstore():
    """
    Load an existing FAISS index or create a new one.
    Rebuilds the index if source documents are newer than the cached index.

    Returns:
        FAISS: A vectorstore ready to be used for retrieval.
    """
    persist_dir = VECTORSTORE_PATH
    index_path = os.path.join(persist_dir, "index.faiss")

    # If an index already exists
    if os.path.exists(index_path):
        index_mtime = os.path.getmtime(index_path)  # last modification of index

        # Get the last modification among all docs
        docs_mtime = max(
            os.path.getmtime(os.path.join(DOCS_PATH, f))
            for f in os.listdir(DOCS_PATH)
        )

        # If docs were updated after the index → rebuild
        if docs_mtime > index_mtime:
            print("📌 Detected document update → rebuilding FAISS index...")
            docs = load_documents()
            db = FAISS.from_documents(docs, embeddings)
            db.save_local(persist_dir)
            return db
        else:
            print("✅ Using cached FAISS index (no updates in docs).")
            return FAISS.load_local(
                persist_dir,
                embeddings,
                allow_dangerous_deserialization=True
            )
    else:
        print("📌 No index found → creating new FAISS index...")
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


def parse_llm_response(response: str):
    """
    Parse the LLM response to extract brand name, slogan, logo mark, color, and branding concept.

    Args:
        response (str): Raw LLM output.

    Returns:
        tuple: (name, slogan, concept, logo_mark, color)
    """
    # First try the expected format (with **)
    name_match = re.search(r"\*\*Brand Name:\*\*\s*(.+)", response)
    slogan_match = re.search(r"\*\*Slogan:\*\*\s*(.+)", response)
    logo_mark = re.search(r"\*\*Logo Mark:\*\*\s*(.+)", response)
    color = re.search(r"\*\*Color:\*\*\s*(.+)", response)
    concept_match = re.search(r"\*\*Branding Concept:\*\*\s*(.+)", response, re.DOTALL)

    # If not found, try looser formats
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
    color = color.group(1).strip() if color else "Color not generated"
    concept = concept_match.group(1).strip() if concept_match else "Concept not generated"

    return name, slogan, concept, logo_mark, color


def generate_branding(description: str):
    """
    Generate branding elements (name, slogan, concept, logo mark, color) 
    based on a user description and reference documents.

    Args:
        description (str): The brand/business description provided by the user.

    Returns:
        dict: A dictionary with branding information.
    """
    # Retrieve relevant docs (top k summaries)
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
- Follow this exact format:

**Brand Name:** <creative brand name>  
**Slogan:** <short impactful slogan>
**Logo Mark: <basic logo mark>**
**Color:** <white, black, green, red, mint, bright, light, spring, aqua, soft, summer, orange, coastal, cream, warm, pink, blue, neutral, elegant, pastel OR vibrant>
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