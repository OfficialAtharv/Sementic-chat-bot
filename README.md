# 🤖 Antiq AI — Retrieval-Augmented Generation (RAG) Chatbot

Antiq AI is a smart, minimal, and modern AI chatbot built using **FastAPI + React** that answers user queries strictly based on provided knowledge using **Retrieval-Augmented Generation (RAG)**.

It combines **semantic search** with a **language model** to give accurate, grounded responses — similar in experience to tools like ChatGPT, Copilot, and Gemini, but fully custom-built.

---

## ✨ Features

- 🔍 **Semantic Search (FAISS + Embeddings)**
- 🧠 **RAG-based Answering (No Hallucinations)**
- 💬 **Modern Chat UI (Copilot / Gemini style)**
- ⚡ **FastAPI Backend**
- 🎨 **Custom UI with Typing Animation**
- 📜 **Auto-scroll to latest message**
- 🔁 **Multi-turn Conversation Support**
- 🧩 **Clean & Short Answers**
- 🖼️ **Custom Antiq AI Logo**
- 🌐 **CORS-enabled Frontend ↔ Backend Connection**

---

## 🏗️ Tech Stack

### Backend
- **FastAPI**
- **Sentence Transformers** (`all-MiniLM-L6-v2`)
- **FAISS** (Vector similarity search)
- **Hugging Face Transformers**
- **FLAN-T5 Base**
- **NumPy**

### Frontend
- **React.js**
- **CSS (Modern dark UI)**
- **Fetch API**
- **Typing indicator animation**
- **Auto-scroll logic (useRef + useEffect)**

---

## 🧠 How RAG Works in Antiq AI

1. User enters a question
2. Question is converted into embeddings
3. FAISS retrieves the most relevant documents
4. Retrieved context + question is sent to the LLM
5. Model answers **only using the retrieved context**
6. If answer is not found →  
   > _"I don't know based on the given data."_

This ensures **accuracy and no hallucination**.

---



UI Highlights
. Right-aligned User messages
. Left-aligned AI responses
. Typing animation (Antiq AI is thinking...)
. Smooth auto-scroll
. Dark gradient background
. Clean spacing & readable fonts

<img width="1909" height="913" alt="image" src="https://github.com/user-attachments/assets/fced8dba-b433-4f1e-b63e-2912d93c1e5c" />


