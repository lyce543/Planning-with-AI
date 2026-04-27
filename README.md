# GitHub Code Analyzer

A web tool for exploring and querying GitHub repositories using AI. Clone any public repository, browse its files, and ask questions about the codebase — answers are generated in real time using RAG (Retrieval-Augmented Generation) powered by OpenAI.

## Features

- **Repository cloning** — paste a GitHub URL, the repo is cloned and indexed automatically
- **File explorer** — browse the full directory tree with a VS Code-style interface
- **Code viewer** — open any file with line numbers and syntax-aware display
- **AI chat** — ask questions about the code and receive streaming answers grounded in the actual source
- **RAG pipeline** — FAISS vector store + OpenAI embeddings ensure answers reference real code, not hallucinations

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Uvicorn |
| AI / LLM | OpenAI GPT-4o |
| Embeddings | OpenAI text-embedding-3-small |
| Vector store | FAISS (via langchain-community) |
| Orchestration | LangChain |
| Frontend | Vanilla HTML/CSS/JS |

## Prerequisites

- Python 3.10+
- Git installed and available in PATH
- OpenAI API key

## Installation

```bash
git clone https://github.com/lyce543/Planning-with-AI.git
cd Planning-with-AI
pip install -r requirements.txt
Configuration
Create a .env file in the project root:


OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o
OPENAI_MODEL is optional — defaults to gpt-4o.

Running

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Open http://localhost:8000 in your browser.

Windows users: if you see a Unicode error in the terminal, prefix the command with set PYTHONUTF8=1 &&

Usage
Paste a public GitHub repository URL into the top bar and click Load
Wait for cloning and indexing to complete (status indicator updates in real time)
Browse files in the left panel — click any file to view its contents
Ask questions about the code in the right-side chat panel
Project Structure

├── app/
│   ├── main.py          # FastAPI app, CORS, static files
│   ├── routes.py        # API endpoints (/load_repo, /chat, /get_repo_structure)
│   ├── github_utils.py  # Repository cloning
│   ├── rag_utils.py     # Vector store indexing and retrieval (app-level)
│   └── llm.py           # OpenAI LLM wrappers
├── utils/
│   ├── rag_utils.py     # RAG pipeline (FAISS + embeddings + streaming)
│   ├── llm.py           # Streaming OpenAI client
│   └── github_utils.py  # Git clone helpers
├── frontend/
│   └── index.html       # Single-page UI
├── config.py            # All configuration constants
└── requirements.txt
API Endpoints
Method	Path	Description
POST	/load_repo	Clone and index a repository
GET	/get_repo_structure	Return file tree and contents
POST	/chat	Streaming chat (SSE)
POST	/clear_repo	Remove cloned repo and vector store
GET	/debug/status	Check current server state
License
MIT
