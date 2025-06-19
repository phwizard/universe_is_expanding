# 🧠 Semantic Continuum Explorer

**Semantic Continuum Explorer** is an experimental interface for exploring the latent knowledge space of a language model — spatially, interactively, and without prompts.

Instead of asking questions or following a linear chatbot flow, users can navigate ideas in 3D semantic space: each idea leads to a constellation of further, related ideas.

---

## 🚀 Project Overview

This system transforms language model outputs into a **navigable, evolving knowledge landscape**.

- Users enter a starting sentence or concept.
- The system generates a wide variety of related ideas (factual, narrative, hypothetical, etc.).
- These ideas are rendered as floating 3D nodes around the central concept.
- Clicking a node recurses: it becomes the new center, and new branches grow around it.

This creates an endless, intuitive way to explore knowledge — ideal for brainstorming, research, learning, or creative thinking.

---

## ⚙️ Technical Architecture

### 🖥️ Frontend (React + React Three Fiber)

- Full-screen 3D canvas built with `react-three-fiber`
- Dynamic user input to set starting concept
- Floating labeled nodes in spherical layout
- Interactive node clicking to regenerate space
- Smooth camera movement using `OrbitControls`

### 🧠 Backend (FastAPI + TinyLlama)

- Language model: [TinyLlama 1.1B Chat](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
- `/expand_continuum` endpoint generates 20+ diverse related ideas for a given input sentence
- Uses `transformers` with `torch` for LLM inference
- Ready for future extensions (FAISS vector indexing, RAG, user session tracking)

---

## 📊 How It Works

![System Diagram](./images/semantic-explorer-architecture.png)

1. **Input**  
   User types a sentence like:  
   > "The universe is expanding."

2. **Generation**  
   The backend uses the LLM to generate a wide range of continuations, such as:
   - "Dark energy may be accelerating this process."
   - "Could the universe collapse back into a singularity?"
   - "What if each galaxy is a neuron?"

3. **Visualization**  
   The frontend displays these ideas as 3D nodes in space, orbiting the central idea.

4. **Interaction**  
   Clicking on any node re-centers the view and generates a new set of semantic neighbors.

---

## 🧪 Setup Instructions

### 1. Backend (FastAPI)

```bash
cd backend/
pip install -r requirements.txt
uvicorn main:app --reload
```

Make sure your `main.py` includes the `/expand_continuum` endpoint.

### 2. Frontend (React + Vite)

```bash
cd frontend/
npm install
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173)

---

## 🛠️ Requirements

- Python 3.10+
- Node.js 18+
- GPU recommended for local LLM inference (or switch to GPT API for cloud inference)
- Tested with Chrome and Firefox

---

## 🧭 Future Ideas

- 🔗 Semantic connections between nodes (edges/lines)
- 🧠 Use real vector embeddings for spatial layout
- 📖 Save & reload semantic journeys (exploration graphs)
- 🌐 Add RAG: connect ideas to real sources (Wikipedia, ArXiv)
- 🎨 Visual themes (cosmic, neural, biological)
- 👓 VR or WebXR support for immersive exploration

---

## 📄 License

MIT License — explore freely, fork boldly, credit kindly.

---

## 🧑‍🚀 Authors

- Taras Filatov (Idea, Architecture, React/LLM Integration)
- OpenAI GPT-4 (Assistance, Code, and Documentation Support)
