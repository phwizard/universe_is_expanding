import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import plotly.express as px
import numpy as np

# Load model and tokenizer
@st.cache_resource
def load_model():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    # Mean pooling over tokens in the final hidden state
    hidden = outputs.hidden_states[-1].squeeze(0)
    return hidden.mean(dim=0).cpu().numpy()

def expand_ideas(prompt):
    input_ids = tokenizer.encode(prompt + "\n-", return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_new_tokens=60, do_sample=True, temperature=0.8)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    lines = [line.strip("- ") for line in generated_text.split("\n") if line.startswith("-")]
    return lines if lines else [generated_text.strip()]

st.title("🧠 Semantic Space Explorer")

sentence = st.text_input("Enter a sentence to explore:", "The universe is expanding.")

if st.button("Explore"):
    st.write("Generating semantic neighbors...")
    base_embedding = get_embedding(sentence)
    ideas = expand_ideas(f"List related facts or expansions about: '{sentence}'")

    embeddings = [base_embedding] + [get_embedding(idea) for idea in ideas]
    labels = ["You"] + ideas

    num_points = len(embeddings)
    perplexity = min(5, max(2, num_points - 1))
    tsne = TSNE(n_components=3, random_state=42, perplexity=perplexity)
    reduced = tsne.fit_transform(np.array(embeddings))

    fig = px.scatter_3d(x=reduced[:,0], y=reduced[:,1], z=reduced[:,2], text=labels,
                        labels={'x': 'X', 'y': 'Y', 'z': 'Z'}, title="3D Semantic Map")
    st.plotly_chart(fig)

    st.subheader("Semantic Branches")
    for i, idea in enumerate(ideas):
        st.markdown(f"**{i+1}.** {idea}")
