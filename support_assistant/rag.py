import os
import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "support_assistant/chroma_db"
DOCS_DIR = "support_assistant/docs"

def get_chroma_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    collection_name = "support_policies"
    
    # Get or create collection
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        collection = client.create_collection(name=collection_name)
        
    # Ingest documents if collection is empty
    if collection.count() == 0:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        docs, ids, metadatas = [], [], []
        
        if os.path.exists(DOCS_DIR):
            for filename in os.listdir(DOCS_DIR):
                if filename.endswith(".txt"):
                    path = os.path.join(DOCS_DIR, filename)
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                        doc_id = filename.replace(".txt", "")
                        docs.append(text)
                        ids.append(doc_id)
                        metadatas.append({"source": filename})
                        
            if docs:
                embeddings = model.encode(docs).tolist()
                collection.add(
                    documents=docs,
                    embeddings=embeddings,
                    ids=ids,
                    metadatas=metadatas
                )
                print(f"Successfully ingested {len(docs)} policy documents into ChromaDB.")
                
    return collection

def query_rag(query_text: str, n_results: int = 2):
    collection = get_chroma_collection()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query_text]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    retrieved_docs = results["documents"][0] if results["documents"] else []
    sources = results["metadatas"][0] if results["metadatas"] else []
    
    context = "\n\n".join(retrieved_docs)
    source_ids = [s.get("source", "unknown") for s in sources]
    return context, source_ids