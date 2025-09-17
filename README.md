# <img src="https://cdn-icons-png.flaticon.com/512/18310/18310909.png" width="80"/> llm-brand-generator

An AI-powered branding assistant that generates **brand name, slogan, and concept visuals** from a simple description.  
It uses **LangChain + Ollama** for text generation and (for now) a simple placeholder image generator.  

---

## <img src="https://cdn-icons-png.flaticon.com/512/2837/2837780.png" width="80"/> How to use it?

Simply provide a description of your desired brand AND click on 'Generate Branding':

<div align="center">
<img src="https://thumbs2.imgbox.com/6b/77/OjuWJH4S_t.png" width="70%"/> 
</div>


After approximately one minute, you will receive the recommended items:

- A suggested name
- A suggested slogan
- A branding concept
- A logo mark
- A palette of colors

<div align="center">
<img src="https://thumbs2.imgbox.com/69/df/V77PkJPR_t.png" width="70%"/> 
</div>

## <img src="https://cdn-icons-png.flaticon.com/512/4380/4380529.png" width="80"/> How its works?

In the soon

---

## <img src="https://cdn-icons-png.flaticon.com/512/18310/18310876.png" width="80"/> Project Structure

```
llm-brand-generator/
├─ app.py                # main interface (Streamlit + integration)
├─ agent.py              # LangChain agent + RAG pipeline
├─ assets.py             # base64 images and icons for the interface
├─ pollinations_api.py   # image generation (Pollinations.ai)
├─ colormagic_api.py     # integration with ColorMagic API (color palettes)
├─ embeddings/           # scripts to generate embeddings
│   └─ build_embeddings.py
│
├─ docs/                 # reference documents (PDF, TXT)
│   ├─ branding_guide.txt
│   └─ marketing_tips.pdf
│
├─ requirements.txt      # project dependencies
└─ vectorstore/          # FAISS store (created automatically)
   └─ index.faiss
```

## <img src="https://cdn-icons-png.flaticon.com/512/7778/7778962.png" width="80"/>  Setup

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

### <img src="https://cdn-icons-png.flaticon.com/512/4380/4380708.png" width="80"/> Debug

- Basic way: just run this command

```
streamlit run app.py --logger.level=debug

```

- Step by step (VS Code): create a .vscode/ folder and inside create a launch.json file with:

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Streamlit",
      "type": "python",
      "request": "launch",
      "program": "app.py",
      "args": [
        "run",
        "app.py",
        "--logger.level=debug"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```

For conditional parts, just use something trivial like if 2 > 1 to ensure the code executes and logging continues.

- Interactive debug (terminal only): this will pause execution in the terminal, and you can inspect variables step by step.

```
import pdb; pdb.set_trace()
```

<hr/>

<div align="center">
  <img src="https://i.ibb.co/kgNSnpv/git-support.png">
</div>
