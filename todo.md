# ✅ TODO: Semantic Continuum Explorer

This file tracks our open ideas, features, and technical enhancements.

---

## 🔨 In Progress

- [ ] Replace hardcoded "universe is expanding" with dynamic user input (✅ done)
- [ ] Backend endpoint `/expand_continuum` for diverse idea generation (✅ done)
- [ ] Frontend support for dynamic idea expansion in 3D (✅ done)

---

## 🧠 Feature Ideas (Planned)

- [ ] Draw semantic **lines between nodes** to show exploration history or relations
- [ ] Add **breadcrumb trail** or navigation path on screen
- [ ] **Visual labels** for node categories (optional tagging later)
- [ ] Animate transitions when re-centering the graph
- [ ] Save and reload semantic graphs from session JSON
- [ ] Allow user to **bookmark favorite ideas**
- [ ] Add **RAG support** to anchor results in real documents/web
- [ ] Enable switching to other LLMs (GPT-4, Phi-2, Mistral, etc.)
- [ ] WebXR or VR mode (navigate space in immersive 3D)
- [ ] Better spatial layout based on **real embedding vectors**
- [ ] Improve visual theming: cosmic, neural, biological modes
- [ ] Add loading spinners or transitions for LLM wait time

---

## 🧪 Research + Technical Exploration

- [ ] Evaluate clustering idea responses automatically (KMeans, cosine similarity)
- [ ] Test cosine spacing using FAISS or sentence-transformers
- [ ] Train custom embedding space to tune semantic layout
- [ ] Prototype "semantic search + fly to node" interface
- [ ] Consider multimodal input: text + image

---

## 🗂️ Low Priority / Experimental

- [ ] Audio narration of nodes (TTS integration)
- [ ] Add multi-user shared session view
- [ ] Deploy on Hugging Face Spaces or Vercel + Render combo

---

## ✅ Completed

- [x] Create 3D interface using React Three Fiber
- [x] Connect frontend to FastAPI backend
- [x] Add `/expand_continuum` API
- [x] Generate 15–25 diverse ideas per sentence
- [x] Recenter view when clicking a node
- [x] Add README with system description and architecture
- [x] Add architecture diagram image
