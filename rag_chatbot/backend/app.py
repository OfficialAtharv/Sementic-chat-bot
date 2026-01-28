from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

# ✅ CORS MUST BE HERE (immediately after app creation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend working"}

# -----------------------
# Load everything ONCE
# -----------------------
documents = [
    "Semantic search understands the meaning of text instead of exact keywords.",
    "Embeddings are numerical representations of text meaning.",
    "Vector databases store embeddings and allow similarity search.",
    "Large Language Models generate human-like responses.",
    "RAG combines search results with language models to produce accurate answers."
]

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(documents)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

chat_model = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_new_tokens=200
)

# -----------------------
# Request Body
# -----------------------
class ChatRequest(BaseModel):
    query: str

# -----------------------
# API Endpoint
# -----------------------
@app.post("/chat")
def chat(request: ChatRequest):
    query_embedding = embed_model.encode([request.query])
    distances, indices = index.search(np.array(query_embedding), k=2)

    context = "\n".join([documents[i] for i in indices[0]])

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{request.query}
Answer:
"""

    result = chat_model(prompt)
    return {"answer": result[0]["generated_text"]}
