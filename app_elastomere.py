import streamlit as st
import pandas as pd

# 1. Configuration de l'interface
st.set_page_config(page_title="Expert Sélecteur EJS", layout="wide")

st.title("🧪 Expert Sélecteur EJS")
st.subheader("Classement par Performance Chimique (Meilleurs en haut)")

# --- BASE DE DONNÉES (Structure stable 17 lignes) ---
data = {
    "Famille Générique": [
        "EPDM", "NBR", "Viton™ A", "Viton™ GF-S", "Viton™ GFLT-S", "Viton™ Extreme ETP", 
        "HNBR", "AFLAS (FEPM)", "FFKM (Chimie Std)", "FFKM (Alimentaire/Vapeur)", 
        "FFKM (Haute Temp)", "Silicone (VMQ)", "PTFE", 
        "Fluorosilicone (FMVQ)", "Silicone Phénylé (PMVQ)", "Caoutchouc Naturel (NR)", "Polyuréthane (AU)"
    ],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "70 ShA", "80 ShA", "75 ShA", "75 ShA", "80 ShA", "70 ShA", "60 ShD", "70 ShA", "70 ShA", "65 ShA", "90 ShA"],
    "Couleur": ["Noir", "Noir", "Noir", "Vert", "Noir", "Noir", "Noir", "Noir", "Noir", "Blanc", "Noir", "Rouge", "Blanc", "Bleu", "Gris", "Blond", "Ocre"],
    "Spécificité": ["Alimentaire", "Standard", "Standard", "Chimie Sévère", "Basse Temp", "Total Fluor", "Pétrole", "Vapeur/Base", "Universel", "FDA/USP VI", "HT 320°C", "FDA", "Total", "Hydrocarbures/Froid", "Extrême Froid", "Mécanique", "Abrasion"],
    "Temp Min": [-50, -30, -20, -15, -15, -35, -40, -10, -20, -15, -10, -60, -200, -60, -100, -50, -30],
    "Temp Max": [150, 100, 200, 230, 200, 230, 150, 200, 260, 250, 320, 200, 260, 175, 200, 80, 100],
    
    # --- FLUIDES ---
    "SANS CHOIX": [0]*17,
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 4, 4, 3, 2],
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5, 2, 3, 1, 1],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5, 2, 2, 2, 1],
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5, 4, 3, 1, 1]
}

# Mapping commercial
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM", "EJS-N70": "NBR", "EJS-V70": "Viton™ A",
    "EJS-V75GF": "Viton™ GF-S", "EJS-V75GFLT": "Viton™ GFLT-S",
    "EJS-V75ETP": "Viton™ Extreme ETP", "EJS-AF80": "AFLAS (FEPM)",
    "EJS-K75CH": "FFKM (Chimie Std)", "EJS-K75AL": "FFKM (Alimentaire/Vapeur)",
    "EJS-K80HT": "FFKM (Haute Temp)", "EJS-H70": "HNBR", "EJS-S70": "Silicone (VMQ)", 
    "EJS-P70": "PTFE", "EJS-FS70": "Fluorosilicone (FMVQ)", 
    "EJS-PS70": "Silicone Phénylé (PMVQ)",
    "EJS-NR65": "Caoutchouc Naturel (NR)", "EJS-AU90": "Polyuréthane (AU)"
}

df = pd.DataFrame(data)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    fluides = sorted([c for c in df.columns if c not in ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max"]])
    
    f1 = st.selectbox("Fluide 1", fluides, index=0)
    f2 = st.selectbox("Fluide 2", fluides, index=fluides.index("SANS CHOIX"))
    t_serv = st.slider("Température de service (°C)", -200, 350, 20)
    
    ref_ejs = st.selectbox("Référence EJS", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs]

# --- CALCUL ET TRI PAR SCORE (IMPORTANT) ---
df["Score"] = df[f1] + df[f2]
# Tri par score décroissant pour mettre les meilleurs (VERTS) en premier
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE ---
st.info(f"Analyse pour: {f1} {'+ ' + f2 if f2 != 'SANS CHOIX' else ''}")

for _, row in df_tri.iterrows():
    is_ref = famille_cible == row["Famille Générique"]
    # Suppression du NameError 'temp' par l'utilisation de t_serv
    temp_ok = row["Temp Min"] <= t_serv <= row["Temp Max"]
    seuil_v = 4 if f2 == "SANS CHOIX" else 8
    
    if not temp_ok:
        bg = "rgba(220, 53, 69, 0.7)" # Rouge
    elif row["Score"] >= seuil_v:
        bg = "rgba(40, 167, 69, 0.7)" # Vert
    else:
        bg = "rgba(253, 126, 20, 0.7)" # Orange

    border = "6px solid white" if is_ref else "none"

    # Construction HTML sécurisée (sans triple guillemets) pour éviter SyntaxError
    html
