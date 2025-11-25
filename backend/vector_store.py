import chromadb
import uuid
from sentence_transformers import SentenceTransformer

# Persistent DB (stored locally on disk)
client = chromadb.PersistentClient(path="vector_store")

collection = client.get_or_create_collection(name="qa_knowledge_base")

# Local embedding model (Free)
model = SentenceTransformer("all-MiniLM-L6-v2")


def add_embedded_text(text: str, source: str):
    """
    Stores text chunks with embeddings in vector DB.
    """
    embedding = model.encode([text])
    
    doc_id = f"{source}_{uuid.uuid4()}"  # safer than hash()
    
    collection.add(
        documents=[text],
        embeddings=embedding,
        metadatas=[{"source": source}],
        ids=[doc_id]
    )

    print(f"[INDEXED] {source} → {doc_id}")


def query_text(query: str, n: int = 5):
    """
    Retrieves most relevant stored chunks based on semantic similarity.
    """
    embedding = model.encode([query])

    results = collection.query(
        query_embeddings=embedding,
        n_results=n
    )

    if not results or not results.get("documents"):
        print("[WARN] No relevant context retrieved.")
        return {"documents": []}

    print(f"[RETRIEVED] {len(results['documents'])} chunks matched.")
    return results
