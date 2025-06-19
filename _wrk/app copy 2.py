import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import cosine_similarity
from umap import UMAP
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
    hidden = outputs.hidden_states[-1].squeeze(0)
    return hidden.mean(dim=0).cpu().numpy()

def expand_ideas(prompt):
    input_ids = tokenizer.encode(prompt + "\n-", return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_new_tokens=60, do_sample=True, temperature=0.8)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    # Extract lines that start with "-"
    lines = [line.strip("- ").strip() for line in generated_text.split("\n") if line.strip().startswith("-")]
    return lines if lines else [generated_text.strip()]

# Streamlit UI
st.title("🧠 Semantic Space Explorer")

sentence = st.text_input("Enter a sentence to explore:", "The universe is expanding.")

if st.button("Explore"):
    st.write("Generating semantic neighbors...")
    base_embedding = get_embedding(sentence)
    
    ideas = expand_ideas(f"List related facts or expansions about: '{sentence}'")
    valid_ideas = [idea for idea in ideas if idea and isinstance(idea, str)]

    if not valid_ideas:
        st.error("No valid expansions were generated. Please try a different sentence.")
    else:
        embeddings = [base_embedding] + [get_embedding(idea) for idea in valid_ideas]

        if len(embeddings) < 3:
            st.warning("Not enough data to visualize in 3D. Please try again with a different sentence.")
        else:
            n_neighbors = max(2, min(5, len(embeddings) - 1))
            reducer = UMAP(n_components=3, n_neighbors=n_neighbors, random_state=42)
            reduced = reducer.fit_transform(np.array(embeddings))

            labels = ["You"] + valid_ideas
            fig = px.scatter_3d(x=reduced[:, 0], y=reduced[:, 1], z=reduced[:, 2], text=labels,
                                labels={'x': 'X', 'y': 'Y', 'z': 'Z'}, title="3D Semantic Map")
            st.plotly_chart(fig)

        st.subheader("Semantic Branches")
        for i, idea in enumerate(valid_ideas):
            st.markdown(f"**{i+1}.** {idea}")
