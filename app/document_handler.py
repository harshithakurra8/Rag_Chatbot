import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from app.config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, EMBEDDING_DIM

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_qdrant_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
    )

def chunk_text(text, max_length=300):
    sentences = text.split(". ")
    chunks, chunk = [], ""
    for sent in sentences:
        if len(chunk) + len(sent) < max_length:
            chunk += sent + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sent + ". "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def embed_text(text):
    return model.encode(text).tolist()

def upload_document(file):
    content = file.file.read().decode("utf-8")
    chunks = chunk_text(content)
    print(f"Chunks: {chunks}")
    points = []
    for chunk in chunks:
        vector = embed_text(chunk)
        points.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {"text": chunk}
        })
    print(f"Points: {points}")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return {"message": "Document uploaded and stored."}

def retrieve_relevant_chunks(query, top_k=3):
    print(f"Retrieving for query: {query}")
    query_vector = embed_text(query)
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    print(f"Search result: {search_result}")
    return [hit.payload["text"] for hit in search_result]
