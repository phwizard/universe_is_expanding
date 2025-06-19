# (c) DeepX, Taras Filatov, 2025
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import numpy as np
import faiss
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS for your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ← Change to "*" only for dev/testing if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load LLM and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

# Get embedding function
@torch.no_grad()
def get_embedding(text: str):
    tokens = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**tokens, output_hidden_states=True)
    hidden = outputs.hidden_states[-1].squeeze(0)
    return hidden.mean(dim=0).cpu().numpy()

# In-memory FAISS index
DIM = model.config.hidden_size
index = faiss.IndexFlatL2(DIM)
sentence_store = []

# Request schemas
class TextRequest(BaseModel):
    sentence: str

class EmbedRequest(BaseModel):
    sentence: str
    neighbors: int = 5

# Expand ideas using LLM
@app.post("/expand")
def expand_ideas(req: TextRequest):
    prompt = req.sentence + "\n-"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_new_tokens=60, do_sample=True, temperature=0.8)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    lines = [line.strip("- ").strip() for line in generated_text.split("\n") if line.strip().startswith("-")]
    return {"ideas": lines if lines else [generated_text.strip()]}

# Embed a sentence into FAISS
@app.post("/embed")
def embed_sentence(req: EmbedRequest):
    emb = get_embedding(req.sentence)
    sentence_store.append(req.sentence)
    index.add(np.array([emb]).astype(np.float32))
    return {"message": "Sentence embedded and added."}

# Search for neighbors using FAISS
@app.post("/search")
def search_neighbors(req: EmbedRequest):
    if index.ntotal == 0:
        return {"neighbors": []}
    emb = get_embedding(req.sentence).astype(np.float32).reshape(1, -1)
    D, I = index.search(emb, req.neighbors)
    results = [sentence_store[i] for i in I[0] if i < len(sentence_store)]
    return {"neighbors": results}

@app.post("/expand_continuum")
def expand_continuum(req: TextRequest):
    # Broader, diverse prompt
    prompt = f"Generate a wide variety of interesting, creative, factual, or hypothetical ideas related to:\n'{req.sentence}'\n-"
    
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_new_tokens=150,
            do_sample=True,
            temperature=1.0,
            top_k=50,
            top_p=0.95
        )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    lines = [
        line.strip("- ").strip()
        for line in generated_text.split("\n")
        if line.strip().startswith("-")
    ]

    # Fallback if bullets fail
    if not lines:
        sentences = generated_text.split(".")
        lines = [s.strip() for s in sentences if len(s.strip()) > 10]

    return {"nodes": lines}

