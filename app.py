import json
import os
import streamlit as st
from dotenv import load_dotenv

from utils.memory import load_history, save_history
from utils.evaluator import evaluate_offer_text
from models.llm_grop import chat_with_groq   

# Load .env
load_dotenv()

# ---------------- Page config ----------------
st.set_page_config(page_title="Négociateur IA (GROQ)", layout="wide")
st.title("💰 Négociateur IA — Multi scénarios (GROQ)")

# ---------------- Load scenarios ----------------
with open(os.path.join("data", "scenarios.json"), "r", encoding="utf-8") as f:
    SCENARIOS = json.load(f)["scenarios"]

scenario_map = {s["titre"]: s for s in SCENARIOS}

with open(os.path.join("data", "intro.json"), "r", encoding="utf-8") as f:
    INTRO = json.load(f)["intro"]

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Clé API Groq", type="password")
    model_name = st.selectbox("Modèle (GROQ)", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    temperature = st.slider("Température", 0.0, 1.0, 0.6)
    selected_title = st.selectbox("Choisir un scénario", list(scenario_map.keys()))

    if st.button("Nouvelle négociation"):
        save_history([])
        st.rerun()

# ---------------- Active scenario ----------------
SC = scenario_map[selected_title]
st.subheader(SC["titre"])
st.markdown(f"**Produit** : {SC['produit']}")
#st.markdown(f"**Client** : {SC['client_type']}")
#st.markdown(f"**Objectif** : {SC['objectif']}")
#st.markdown(f"**Prix affiché** : {SC['prix']} € — **Prix minimal** : {SC['prix_min']} €")

# ---------------- System prompt ----------------
with open(os.path.join("prompts", "sell_prompt.txt"), "r", encoding="utf-8") as f:
    base_template = f.read()

system_prompt = base_template.format(
    produit=SC["produit"],
    client_type=SC["client_type"],
    objectif=SC["objectif"],
    instructions=SC.get("prompt_system", "")
)

# ---------------- Chat memory ----------------
history = load_history()  # list of dicts {"role","content"}

st.divider()
st.subheader("Conversation")

if not history: 
    st.chat_message("assistant").write(INTRO)

# show messages
for msg in history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ---------------- User input ----------------
user_input = st.chat_input("Votre message...")

if user_input:
    # Save user message to UI and history
    st.chat_message("user").write(user_input)
    history.append({"role": "user", "content": user_input})

    # API key check
    if not groq_api_key:
        st.sidebar.error("Entrez votre clé GROQ dans la sidebar pour appeler le modèle.")
    else:
        # Call GROQ
        assistant_text = chat_with_groq(
            system_prompt=system_prompt,
            history=history[:-1],  # pass previous messages; user_input already appended but we prefer previous
            user_message=user_input,
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=temperature
        )

        # Show assistant message
        st.chat_message("assistant").write(assistant_text)
        history.append({"role": "assistant", "content": assistant_text})

        # Save history
        save_history(history)

        # Evaluate user's offer if present (simple evaluation)
        eval_result = evaluate_offer_text(user_input, SC)
        st.sidebar.markdown("### Évaluation de l'offre utilisateur")
        st.sidebar.json(eval_result)
