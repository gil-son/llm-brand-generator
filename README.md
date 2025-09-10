# llm-brand-generator

# 🤖 llm-brand-generator

An AI-powered branding assistant that generates **brand name, slogan, and concept visuals** from a simple description.  
It uses **LangChain + Ollama** for text generation and (for now) a simple placeholder image generator.  

---

## 📂 Project Structure

```
llm-brand-generator/
├─ app.py          # interface e integração
├─ agent.py        # LangChain agent + RAG pipeline
├─ embeddings/     # scripts para gerar embeddings
├─ vectorstore/    # FAISS store        
├─ docs/           # documentos de referência (PDF, TXT)
│   ├─ branding_guide.txt
│   └─ marketing_tips.pdf
├─ requirements.txt
└─ vectorstore/ # Will be created automatically

```

## ⚙️ Setup

### 1. Create a virtual environment

```
cd llm-brand-generator/
python3 -m venv venv
```

### 2. Activate the environment

```
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```
streamlit run app.py

### 4. Run the app

```
streamlit run app.py
```