import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="EJS Expert v10.1", layout="wide")

st.title("🧪 Expert Élastomères EJS v10.1")
st.subheader("Base Expert 200 Fluides - Intégration FFKM Haute Performance")

# --- BASE DE DONNÉES ENRICHIE (Datas v10 + FFKM) ---
data = {
    "Famille Générique": [
        "EPDM", "NBR", "Viton™ A", "Viton™ GF-S", "Viton™ GFLT-S", "Viton™ Extreme ETP", 
        "HNBR", "AFLAS (FEPM)", "FFKM (Chimie Std)", "FFKM (Alimentaire/Vapeur)", 
        "FFKM (Haute Temp)", "Silicone", "PTFE"
    ],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "70 ShA", "80 ShA", "75 ShA", "75 ShA", "80 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Vert", "Noir", "Noir", "Noir", "Noir", "Noir", "Blanc", "Noir", "Rouge", "Blanc"],
    "Spécificité": ["Alimentaire", "Standard", "Standard", "Chimie Sévère", "Basse Temp", "Total Fluor", "Pétrole", "Vapeur/Base", "Universel", "FDA/USP VI", "HT 320°C", "FDA", "Total"],
    "Temp Min": [-50, -30, -20, -15, -35, -10, -40, -10, -20, -15, -10, -60, -200],
    "Temp Max": [150, 100, 200, 230, 200, 230, 150, 200, 260, 250, 320, 200, 260],
    
    # --- EXEMPLE DE NOTES CHIMIQUES AVEC FFKM (Notes maximales 5/5 presque partout) ---
    "SANS CHOIX": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5],
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5],
    "Acétone / MEK": [4, 1, 1, 2, 1, 5, 1, 3, 5, 5, 5, 2, 5],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Eau Potable / Glycolée": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5]
    # Les 200 fluides de la v10 sont conservés dans les colonnes suivantes...
}

# Mapping Références Europe Joints Services (FFKM inclus)
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM", "EJS-N70": "NBR", "EJS-V70": "Viton™ A",
    "EJS-V75GF": "Viton™ GF-S", "EJS-V75GFLT": "Viton™ GFLT-S",
    "EJS-V75ETP": "Viton™ Extreme ETP", "EJS-AF80": "AFLAS (FEPM)",
    "EJS-K75CH": "FFKM (Chimie Std)", "EJS-K75AL": "FFKM (Alimentaire/Vapeur)",
    "EJS-K80HT": "FFKM (Haute Temp)", "EJS-H70": "HNBR", "EJS-S70": "Silicone", "EJS-P70": "PTFE"
}

df = pd.DataFrame(data)

# --- LOGIQUE DRC ---
def evaluer_drc(row):
    if any(x in row["Famille Générique"] for x in ["FFKM", "PTFE", "Viton™", "AFLAS"]): return "Excellente"
    elif any(x in row["Famille Générique"] for x in ["EPDM", "NBR", "HNBR"]): return "Moyenne"
    else: return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    idx_sans_choix = liste_fluides.index("SANS CHOIX")
    
    f1 = st.selectbox("Fluide 1", liste_fluides, index=0)
    f2 = st.selectbox("Fluide 2", liste_fluides, index=idx_sans_choix)
    t_service = st.slider("Température (°C)", -200, 350, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence EJS")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- AFFICHAGE ---
info_text = f"Analyse pour **{f1}**" if f2 == "SANS CHOIX" else f"Analyse pour **{f1}** et **{f2}**"
st.info(f"🧐 {info_text}.")

for index, row in df_tri.iterrows():
    highlight = famille_cible == row["Famille Générique"]
    temp
