import streamlit as st
import pandas as pd

# 1. Configuration (Mode large v5.6)
st.set_page_config(page_title="EJS Expert v9.5", layout="wide")

st.title("🧪 Expert Élastomères EJS v9.5")
st.subheader("Base Expert & Agroalimentaire - Jus de Saumure 100%")

# --- BASE DE DONNÉES ENRICHIE (Datas v9.4 + Saumure) ---
data = {
    "Famille Générique": [
        "EPDM", "NBR", "Viton™ A (Standard)", "Viton™ GBL-S", 
        "Viton™ GF-S", "Viton™ GFLT-S", "Viton™ Extreme ETP", 
        "AFLAS (FEPM)", "HNBR", "Silicone", "PTFE"
    ],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "80 ShA", "70 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Noir", "Vert", "Noir", "Noir", "Noir", "Noir", "Rouge", "Blanc"],
    "Spécificité": ["Alimentaire", "Standard", "Standard", "Haute teneur Fluor", "Chimie Sévère", "Basse Température", "Universalité Chimique", "Vapeur/Base", "Pétrole/Chaleur", "FDA", "Total"],
    "Temp Min": [-50, -30, -20, -15, -15, -35, -10, -10, -40, -60, -200],
    "Temp Max": [150, 100, 200, 210, 230, 200, 230, 200, 150, 200, 260],
    
    # --- NOUVEAU FLUIDE ---
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    
    # --- FLUIDES ALIMENTAIRES & NEP ---
    "Vapeur (SEP 140°C)": [5, 1, 2, 2, 3, 2, 4, 5, 3, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    "Eau Potable": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Graisse Animale": [1, 5, 5, 5, 5, 5, 5, 4, 5, 4, 5],
    "Huile Végétale": [1, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Lait / Produits Laitiers": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    
    # --- CHIMIE & INDUSTRIE (Extrait 100 fluides v9.4) ---
    "Acide Sulfurique 98%": [4, 1, 3, 4, 5, 5, 5, 3, 1, 1, 5],
    "Méthanol": [5, 4, 1, 1, 2, 4, 5, 1, 4, 5, 5],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Huile Hydraulique": [1, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5],
    "Acétone": [4, 1, 1, 1, 1, 1, 5, 3, 1, 2, 5],
    "Hypochlorite de Soude": [5, 2, 5, 5, 5, 5, 5, 5, 2, 3, 5],
    # ... conservez ici l'intégralité de vos colonnes fluides existantes
}

# Mapping Références EJS
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM",
    "EJS-N70": "NBR",
    "EJS-V70": "Viton™ A (Standard)",
    "EJS-V75GBL": "Viton™ GBL-S",
    "EJS-V75GF": "Viton™ GF-S",
    "EJS-V75GFLT": "Viton™ GFLT-S",
    "EJS-V75ETP": "Viton™ Extreme ETP",
    "EJS-AF80": "AFLAS (FEPM)",
    "EJS-H70": "HNBR",
    "EJS-S70": "Silicone",
    "EJS-P70": "PTFE"
}

df = pd.DataFrame(data)

# --- LOGIQUE DRC ---
def evaluer_drc(row):
    if any(x in row["Famille Générique"] for x in ["PTFE", "Viton™", "AFLAS"]): return "Excellente"
    elif any(x in row["Famille Générique"] for x in ["EPDM", "NBR", "HNBR"]): return "Moyenne"
    else: return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    st.write("---")
    # Défaut sur Moyenne comme demandé précédemment
    choix_drc = st.multiselect("Filtrer par Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence Commerciale EJS")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list
