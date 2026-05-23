# Agentic RAG System with Agno, Ollama, and LanceDB

A lightweight **agentic Retrieval-Augmented Generation (RAG)** project built with [Agno](https://github.com/agno-agi/agno), [Ollama](https://ollama.com/), and [LanceDB](https://lancedb.github.io/lancedb/). This system can ingest PDF content from a URL (and can be extended to local PDFs), retrieve relevant context, and answer questions using a local LLM.

## Features

- PDF-based knowledge ingestion using `PDFUrlKnowledgeBase`
- Local embeddings with `OllamaEmbedder`
- Vector storage and hybrid retrieval using `LanceDb`
- Local LLM inference through `Ollama`
- Agent-based question answering with references enabled
- Support for conversational context and response history
- Easy extension for website content ingestion or additional document sources

## Tech Stack

- **Framework:** Agno
- **LLM:** Ollama (`gemma3:1b`)
- **Embedding Model:** `mxbai-embed-large`
- **Vector Database:** LanceDB
- **Knowledge Source:** PDF URL / local PDF
- **Language:** Python

## Project Overview

This project demonstrates how to build an agentic RAG pipeline that:

1. Loads a PDF document from a public URL.
2. Converts the content into embeddings using Ollama.
3. Stores the embeddings in LanceDB for retrieval.
4. Uses an Agno agent with a local Ollama model to answer user queries.
5. Returns grounded responses with document-aware context and references.

The current example is configured for an IPL T20 rules PDF and answers questions such as summarizing the super over rule.

## Architecture

```text
User Query
   |
   v
Agno Agent
   |
   +--> Knowledge Base (PDFUrlKnowledgeBase / PDFKnowledgeBase)
              |
              v
         Chunking + Embedding (OllamaEmbedder)
              |
              v
        LanceDB Vector Store (Hybrid Search)
              |
              v
      Relevant Context Retrieved
              |
              v
   Ollama LLM generates grounded answer
```

## Project Structure

```bash
.
├── simple_rag.py
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AshcharyaR/Simple_Agent.git
cd your-repo-name
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install agno lancedb ollama
```

> Depending on your Agno version, you may also need supporting packages for PDF parsing.

### 4. Install and run Ollama

Download Ollama from [ollama.com](https://ollama.com/) and pull the required models:

```bash
ollama pull gemma3:1b
ollama pull mxbai-embed-large
```

## Usage

Run the script:

```bash
python simple_rag.py
```

Before querying the knowledge base for the first time, make sure document loading is enabled if needed:

```python
knowledge_base.load(upsert=True)
```

You can then modify the prompt inside the script:

```python
prompt = "Summarize Super over rule"
```

## Example Code Highlights

### Embedding and Vector DB

```python
embedder = OllamaEmbedder(id="mxbai-embed-large", dimensions=1024)

vector_db = LanceDb(
    table_name="iplt20",
    uri="/tmp/lancedb",
    search_type=SearchType.hybrid,
    embedder=embedder,
)
```

### Knowledge Base

```python
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://documents.iplt20.com/bcci/documents/1775736835406_TATA_IPL_2026_Match_Playing_Conditions.pdf"],
    vector_db=vector_db,
)
```

### Agent Setup

```python
agent = Agent(
    model=Ollama(id="gemma3:1b", options={"num_ctx": 16192}),
    knowledge=knowledge_base,
    add_context=True,
    add_references=True,
    search_knowledge=False,
    add_history_to_messages=True,
    num_history_responses=10,
    markdown=True,
)
```

## Local PDF Support

The project can also be adapted for local PDF files by switching from `PDFUrlKnowledgeBase` to `PDFKnowledgeBase`.

```python
knowledge_base = PDFKnowledgeBase(
    path="path/to/your/file.pdf",
    vector_db=vector_db,
)
```

## Extending to Website Content

To support websites, you can extend the same architecture by adding a web knowledge source supported by Agno, preprocessing webpage text, or crawling pages and storing chunks in the same vector database.

Possible improvements:

- Add multiple PDF sources
- Support both PDF and website URLs
- Build a chat UI with Streamlit or Gradio
- Add citation formatting for answers
- Enable semantic + hybrid retrieval benchmarking
- Add persistent storage and deployment configuration

## Use Cases

- Document question answering
- Policy or rulebook assistants
- Research assistants for PDFs and websites
- Internal knowledge retrieval bots
- Domain-specific AI assistants

## Challenges Solved

This project addresses common RAG development needs such as:

- Running a fully local pipeline with Ollama
- Grounding LLM answers in external knowledge
- Retrieving content from long-form PDF documents
- Maintaining short conversational history in responses
- Building a modular agent workflow with Agno

## Future Improvements

- Add a web page ingestion pipeline
- Create a CLI or web-based chat interface
- Support multi-document indexing
- Add evaluation for retrieval quality
- Dockerize the application
- Deploy as an internal AI assistant

## Author

**Ashcharya Ramteke**  
Machine Learning Enthusiast

## License

This project is open-source and can be released under the MIT License. Update this section based on the license you choose.
