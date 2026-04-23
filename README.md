# RAG-Based Customer Support Assistant

A production-ready Retrieval-Augmented Generation (RAG) system using LangGraph and Human-in-the-Loop escalation for intelligent customer support automation.

## Overview

This system combines:
- **PDF Knowledge Base** - Company documents, FAQs, policies
- **Vector Embeddings** - Semantic search via ChromaDB
- **LLM Generation** - Groq's Llama3-8b for grounded responses
- **LangGraph Workflow** - Graph-based orchestration with conditional routing
- **Human Escalation** - HITL queue for complex/sensitive queries

## Architecture

```
PDF Documents → Chunking → Embeddings → ChromaDB (Vector Store)
                                            ↓
User Query → Flask API → LangGraph → Retriever → LLM → Response
                         ↓
                    HITL Escalation Queue
```

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Groq API key (free at https://console.groq.com/keys)

### 2. Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure

```bash
# Create .env file with your Groq API key
GROQ_API_KEY=your_api_key_here

# Get key from: https://console.groq.com/keys
```

### 4. Add Knowledge Base

```bash
# Create data folder
mkdir data

# Add your PDF to: data/knowledge_base.pdf
# (See data/README.md for detailed instructions)
```

### 5. Run

```bash
python app.py
# Open: http://localhost:5000
```

## Project Structure

```
proj/
├── app.py                    # Flask web application
├── graph.py                  # LangGraph workflow (2-node pipeline)
├── ingest.py                 # PDF ingestion & chunking
├── retriever.py              # Vector database retrieval
├── llm.py                    # LLM response generation
├── hitl.py                   # Human escalation logging
├── config.py                 # Configuration settings
├── requirements.txt          # Dependencies
├── .env                      # API keys (create this)
├── data/
│   ├── knowledge_base.pdf    # Your PDF here
│   └── README.md             # Setup instructions
├── templates/index.html      # Web UI
├── escalations.jsonl         # Escalation logs
├── HLD.pdf                   # High-Level Design
├── LLD.pdf                   # Low-Level Design
├── TECHNICAL_DOCUMENTATION.md # Technical guide
└── README.md                 # This file
```

## API Documentation

### Web Interface

**URL:** `http://localhost:5000/`

### REST API

**Endpoint:** `POST /api/query`

**Request:**
```json
{
  "query": "How do I reset my password?"
}
```

**Response:**
```json
{
  "answer": "Go to login page...",
  "confidence": 0.85,
  "escalate": false
}
```

## Workflow

### Process Node
1. **Retrieve** - Get top-4 chunks from ChromaDB
2. **Generate** - LLM creates answer
3. **Calculate** - Confidence score
4. **Decide** - Escalate if low confidence or sensitive keywords

### Output Node
1. **Check** escalation flag
2. **Return** answer or escalation notice

## Error Handling (LLD Requirements)

| Error | Handling |
|-------|----------|
| **Missing PDF** | Returns error + escalates |
| **No relevant chunks** | Low confidence → escalates |
| **LLM failure** | "Service unavailable" → escalates |
| **Database error** | Fallback response → escalates |
| **Invalid input** | Returns 400 validation error |

## Escalation Logic

Automatically escalates if:
- Confidence < 0.45
- Query contains: 'refund', 'legal', 'complaint'
- No relevant information found
- System error occurred

Escalated queries logged to `escalations.jsonl`

## Configuration

Edit `config.py`:
```python
TOP_K = 4                           # Chunks to retrieve
CONFIDENCE_THRESHOLD = 0.45         # Escalation threshold
MODEL = 'llama3-8b-8192'           # Groq model
CHUNK_SIZE = 500                   # Token size
CHUNK_OVERLAP = 100                # Token overlap
```

## Testing

**FAQ Query (Should auto-respond):**
```
Q: "How do I reset my password?"
Expected: Answer, confidence > 0.7, escalate=false
```

**Escalation Query (Should escalate):**
```
Q: "I want a refund"
Expected: Escalation message, escalate=true
```

## Troubleshooting

### "Place PDF at data/knowledge_base.pdf"
- Create `data/` folder
- Add PDF file named `knowledge_base.pdf`

### "GROQ_API_KEY not found"
- Create `.env` file
- Add: `GROQ_API_KEY=your_key_here`

### "No module named 'langchain'"
```bash
pip install -r requirements.txt
```

## Design Documents

📄 **HLD.pdf** - High-Level Architecture  
📄 **LLD.pdf** - Low-Level Implementation Details  
📄 **TECHNICAL_DOCUMENTATION.md** - Engineering Explanation

## Version

**Version:** 1.0  
**Date:** April 23, 2026  
**Status:** Production-Ready
