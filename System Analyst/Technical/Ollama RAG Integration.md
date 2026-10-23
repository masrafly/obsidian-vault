# 🤖 Ollama + RAG Integration Guide

## Overview
Integrasi local LLM (Ollama) dengan Retrieval-Augmented Generation untuk Document Control SaaS Anda.

---

## Architecture Options

### Option 1: Local RAG Pipeline (Recommended)
```
┌─────────────────┐
│   Obsidian      │
│   Vault         │◄─── Documents & Templates
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   Document      │
│   Loader        │ (Markdown/PDF/HTML)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   Vector DB     │
│   (ChromaDB)    │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   Ollama LLM    │
│   (phi-3,       │
│    mistral,     │
│    llama3)      │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   Generator     │
│   (output to   │
│    vault)      │
└─────────────────┘
```

### Option 2: Web Search + Ollama
```
User Prompt → Web Search → Ollama Context → RAG Enhancement → Generate Document
```

---

## Implementation Steps

### 1. Install Ollama
```bash
# Windows (from D:\Obsidian-Vault)
winget install Ollama.Ollama

# atau download installer dari:
# https://ollama.com/download
```

### 2. Pull LLM Models
```bash
ollama pull phi3:mini          # Fast, good for tasks
ollama pull llama3:latest      # Better quality
ollama pull mistral:7b         # Balanced
```

### 3. Setup Vector Database (ChromaDB)
```bash
pip install chromadb ollama
pip install langchain-community pypdf
pip install python-docx markdown
```

### 4. Document Loader Script
```python
# scripts/ollama_rag.py
import ollama
import chromadb
from pathlib import Path

VAULT_PATH = Path("D:/Obsidian-Vault")
COLLECTION_NAME = "document_control"

def load_documents():
    docs = []
    for md_file in VAULT_PATH.rglob("*.md"):
        content = md_file.read_text()
        docs.append({"id": str(md_file), "text": content})
    return docs

def create_vector_db():
    client = chromadb.PersistentClient(path="D:/Obsidian-Vault/.chromadb")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    
    docs = load_documents()
    collection.add(
        ids=[d["id"] for d in docs],
        documents=[d["text"] for d in docs]
    )
    return client, collection

def query_rag(question, collection):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    
    context = "\n".join(results["documents"][0])
    
    response = ollama.chat(
        model="phi3:mini",
        messages=[{
            "role": "system",
            "content": f"""You are a Document Control assistant.
            Use this context to answer:
            {context}

            Generate appropriate document content based on requirements."""
        }, {
            "role": "user",
            "content": question
        }]
    )
    
    return response["message"]["content"]
```

---

## Integration with Your Workflows

### 1. Auto-RAG Document Generation
```bash
# Setiap kali request baru
python scripts/ollama_rag.py --request "Buatkan drawing untuk ACB 1000A"
```

### 2. Template Completion with RAG
```python
# scripts/generate_with_rag.py
def complete_template(template_vars, user_requirements):
    # Query RAG for similar documents
    similarity = query_rag(user_requirements, collection)
    
    # Fill template with RAG-enhanced context
    completed = template_vars.copy()
    completed["content"] = similarity
    
    return generate_pdf(completed)
```

### 3. Real-time Prompt Enhancement
```bash
# scripts/enhance_prompt.sh
#!/bin/bash
prompt="$1"
enhanced=$(ollama run phi3:mini "
SYSTEM: You are an expert document control engineer.
Enhance this prompt with technical specifications:
$prompt

Return JSON with: requirements, specs, format" | jq -r '.requirements')

python log_session.py "$prompt -> $enhanced"
```

---

## Benefits for Your Use Case

### 1. Drawing Document Generation
- **Auto-detect** voltage/current requirements from PO
- **Suggest** standard content based on similar drawings
- **Verify** compliance with technical specs

### 2. Template Selection
```python
# Otomata pilih template yang paling cocok
template = find_best_template(user_specs)
completed_doc = fill_template(template, user_data)
```

### 3. Revision Detection
```python
# Bandingkan old vs new requirements
changes = detect_changes(old_doc, new_req)
generate_revision_notes(changes)
```

### 4. Transmittal Generation
```python
# Otomat hasilkan daftar dokumen yang dikirim
transmittal = generate_transmittal(documents, client_info)
```

---

## Performance Benchmarks

| Model | RAM Usage | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| phi3:mini | 1GB | Fast | Good | Draft/Generation |
| llama3:8b | 4GB | Medium | Very Good | Final Review |
| mistral:7b | 4GB | Medium | Good | Template Matching |

---

## Setup Commands (Windows)

```bash
# 1. Activate Ollama service
ollama serve &

# 2. Run RAG pipeline
python scripts/ollama_rag.py --init-vault
python scripts/ollama_rag.py --load-documents
python scripts/ollama_rag.py --query "garis tengah untuk ACB"

# 3. Generate document
python scripts/generate_with_rag.py --prompt "Buat drawing ACB" --template "drawing"
```

---

## Tips untuk Windows Environment

1. **Julia Path Issues:**
   ```bash
   set CHROMA_DB_PATH=D:\Obsidian-Vault\.chromadb
   ```

2. **Ollama WSL Integration:**
   ```bash
   # Jika di WSL, forward ke Windows
   export OLLAMA_HOST=http://host.docker.internal:11434
   ```

3. **Auto-start Ollama:**
   - Tambahkan ke Task Scheduler (Startup)
   - Atau gunakan NSSM service

---

## Next Steps

1. [ ] Install Ollama di Windows (`winget install Ollama.Ollama`)
2. [ ] Pull model phi3:mini (`ollama pull phi3:mini`)
3. [ ] Test RAG script (`python scripts/ollama_rag.py --test`)
4. [ ] Integrate ke workflow utama (`scripts/log_session.py`)

---

## Resources

- Ollama Docs: https://ollama.com/docs
- ChromaDB: https://docs.trychroma.com/
- LangChain RAG: https://python.langchain.com/docs/use_cases/question_answering/