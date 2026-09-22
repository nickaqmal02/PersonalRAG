# 🤖 RAG Agent

A personal RAG (Retrieval-Augmented Generation) agent with a beautiful terminal UI.

## ✨ Features

- 📚 **Document Ingestion** - Index PDFs and text files
- 🔍 **Semantic Search** - Find relevant documents with vector search
- 🧠 **LLM Integration** - Powered by Groq LLM
- 🎨 **Beautiful TUI** - Terminal interface with Textual
- 📊 **Source Tracking** - See where answers come from
- 💾 **Persistent Storage** - Vector embeddings saved locally

## 🚀 Quick Start

```bash
git clone https://github.com/nickaqmal02/PersonalRAG.git
cd PersonalRAG
poetry install

# noted that everytime you adding package into pyproject.toml
# you have to run poetry install but but but need to run the 
eval $(poetry env activate)

# copy the example of environment example
cp .env.example .env
# Add your GROQ_API_KEY

```

### Installation

```bash

pip install rag-agent

MIT License

Copyright (c) 2024 nick aqmal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

### DETAIL INTERPRETATION ABOUT MY APPLICATION

```bash
┌─────────────────────────────────────────────────────┐
│                   YOUR PIPELINE                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📄 Documents → 🔧 Preprocess → ✂️ Chunk           │
│       ↓                                             │
│  🔢 Embed → 💾 Store in ChromaDB                    │
│                                                     │
│  ❓ Query → 🔢 Embed → 🔍 Retrieve Top-K            │
│       ↓                                             │
│  📝 Build Context → 🧠 LLM → ✅ Answer              │
│                                                     │
└─────────────────────────────────────────────────────┘

```

##### this is Naive RAG - the classic retrieve then generate pattern

why It's called as Naive 

Because we don't even interrupt the **whole pipeline**


##### THEN HOW TO USE IT ??

## **THE USAGE?**

```bash

eval $(poetry env activate)
# Ingest documents first but you gotta upload the document inside the data/filestype/
poetry run PersonalRAG ingestion

# running the single query
poetry run PersonalRAG chat -q "what is machine learning"

# interactive mode
poetry run PersonalRAG chat -i

# get the status of our application
poetry run PersonalRAG status

# in future we will update the next features of our tui application but for now, cli interactive was enough
poetry run PersonalRAG tui

```

## **TECH STACK**

- Python 3.11+
- ChromaDB (vector store)
- SentenceTransformers (embeddings)
- LangChain (document loading)
- Groq (LLM)
- Click (CLI)
- Poetry (packaging)


