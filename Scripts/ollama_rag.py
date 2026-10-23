#!/usr/bin/env python3
"""
Ollama RAG Integration for Document Control
Place at: D:\Obsidian-Vault\Scripts\ollama_rag.py
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Paths
VAULT_PATH = Path("D:/Obsidian-Vault")
CHROMA_PATH = VAULT_PATH / ".chromadb"
COLLECTION_NAME = "document_control"

try:
    import chromadb
    import ollama
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Run: pip install chromadb ollama")
    sys.exit(1)

def initialize_vector_db():
    """Create or load the vector database"""
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"✅ Loaded existing collection with {collection.count()} documents")
    except:
        collection = client.create_collection(name=COLLECTION_NAME)
        print(f"✅ Created new collection")
    
    return client, collection

def load_vault_documents() -> List[Dict]:
    """Load all markdown and PDF documents from vault"""
    docs = []
    
    # Load Markdown files
    for md_file in VAULT_PATH.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            docs.append({
                "id": str(md_file.relative_to(VAULT_PATH)),
                "text": content,
                "path": str(md_file)
            })
        except Exception as e:
            print(f"⚠ Skipping {md_file}: {e}")
    
    # Load PDFs (basic text extraction)
    for pdf_file in VAULT_PATH.rglob("*.pdf"):
        try:
            import PyPDF2
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = '\n'.join(page.extract_text() for page in reader.pages)
            
            docs.append({
                "id": str(pdf_file.relative_to(VAULT_PATH)),
                "text": text,
                "path": str(pdf_file)
            })
        except Exception as e:
            print(f"⚠ Skipping {pdf_file}: {e}")
    
    print(f"📄 Loaded {len(docs)} documents")
    return docs

def index_documents(collection, docs: List[Dict]):
    """Index documents into vector database"""
    ids = [d["id"] for d in docs]
    texts = [d["text"][:10000] for d in docs]  # Truncate for performance
    
    collection.add(ids=ids, documents=texts)
    print(f"✅ Indexed {len(docs)} documents")

def query_documents(collection, query: str, n_results: int = 5) -> List[Dict]:
    """Query vector database"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return [
        {"id": rid, "text": text}
        for rid, text in zip(results["ids"][0], results["documents"][0])
    ]

def generate_with_ollama(prompt: str, context: str = None, model: str = "phi3:mini"):
    """Generate response using Ollama"""
    messages = [{
        "role": "system",
        "content": """You are an expert document control engineer for electrical equipment.
Generate technical documents following industry standards (IEC, IEEE).
Be precise, use proper technical terminology."""
    }]
    
    if context:
        messages.append({
            "role": "system",
            "content": f"Reference context:\n{context[:2000]}"
        })
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    try:
        response = ollama.chat(model=model, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Ollama RAG for Document Control")
    parser.add_argument("--init", action="store_true", help="Initialize vector DB")
    parser.add_argument("--load", action="store_true", help="Load documents")
    parser.add_argument("--query", type=str, help="Query the database")
    parser.add_argument("--generate", type=str, help="Generate document")
    parser.add_argument("--model", default="phi3:mini", help="Ollama model to use")
    
    args = parser.parse_args()
    
    client, collection = initialize_vector_db()
    
    if args.init:
        print("🚀 Initializing RAG system...")
        docs = load_vault_documents()
        index_documents(collection, docs)
    
    elif args.load:
        print("📚 Loading documents...")
        docs = load_vault_documents()
        index_documents(collection, docs)
    
    elif args.query:
        print(f"🔍 Querying: {args.query[:50]}...")
        results = query_documents(collection, args.query)
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['id']}")
            print(f"   {r['text'][:200]}...")
    
    elif args.generate:
        print(f"🤖 Generating document using {args.model}...")
        results = query_documents(collection, args.generate)
        context = "\n\n".join([r["text"] for r in results[:3]])
        
        response = generate_with_ollama(args.generate, context, args.model)
        if response:
            print("\n" + "="*60)
            print(response)
            print("="*60)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()