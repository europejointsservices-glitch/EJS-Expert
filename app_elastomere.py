import streamlit as st
import pandas as pd

# 1. Configuration (Retour au mode large v5.6)
st.set_page_config(page_title="EJS Expert v6.5", layout="wide")

st.title("🧪 Expert Élastomères EJS v6.5")
st.subheader("Filtre DRC Dynamique & Performance")

# --- BASE DE DONNÉES (Strictement inchangée) ---
data = {
    "Compound EJS": ["EJS-E70P", "EJS-N70", "EJS-V70ETP", "EJS-S70", "EJS-P70"],
    "Famille": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Rouge", "Blanc"],
    "Norme": ["FDA/EC1935", "Standard", "Aeronautique", "FDA", "FDA"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    "Acide Chlorhydrique": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minerale": [1, 5, 5, 2, 5],
    "Vapeur": [5, 1, 2, 3, 5],
}

df = pd.DataFrame(data)

# --- LOGIQUE DE TRADUCTION DRC (Sans changer la base) ---
# On définit ici ce qu'est une DRC excellente ou basse selon le composé
def evaluer_drc(row):
    if "PTFE" in row["Famille"] or "FKM" in row["Famille"]:
        return "Excellente"
    elif "EPDM" in row["Famille"] or "NBR" in row["Famille"]:
        return "Moyenne"
    else:
        return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    f1 = st.selectbox("Sélectionner Fluide 1", [c for c in data if c not in ["Compound EJS", "Famille", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max"]])
    f2 = st.selectbox("Sélectionner Fluide 2", [c for c in data if c not in ["Compound EJS", "Famille", "Dureté
