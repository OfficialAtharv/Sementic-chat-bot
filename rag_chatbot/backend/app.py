from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import numpy as np
import faiss
import torch

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# -----------------------
# App setup
# -----------------------
app = FastAPI()

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
# RAG data
# -----------------------
documents = [
    "Semantic search understands the meaning of text instead of exact keywords.",
    "Embeddings are numerical representations of text meaning.",
    "Vector databases store embeddings and allow similarity search.",
    "Large Language Models generate human-like responses.",
    "RAG combines search results with language models to produce accurate answers."
]

# -----------------------
# Embeddings + FAISS (loaded once)
# -----------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(documents, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# -----------------------
# LLM (FAST & CORRECT)
# -----------------------
MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

model.eval()  # inference mode

# -----------------------
# Request schema
# -----------------------
class ChatRequest(BaseModel):
    query: str

# -----------------------
# Chat endpoint
# -----------------------
@app.post("/chat")
def chat(request: ChatRequest):
    # 1. Embed query
    query_embedding = embed_model.encode(
        [request.query], convert_to_numpy=True
    )

    # 2. Retrieve top-k docs
    _, indices = index.search(query_embedding, k=2)
    context = "\n".join(documents[i] for i in indices[0])

    # 3. Prompt
    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know based on the given data."

Context:
{context}

Question:
{request.query}
Answer:
"""

    # 4. Generate (FAST)
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=40,
            do_sample=False,
            temperature=0.0
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return {"answer": answer.strip()}
