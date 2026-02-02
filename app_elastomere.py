import streamlit as st
import pandas as pd

# 1. Configuration
st.set_page_config(page_title="Expert Sélecteur EJS", layout="wide")

st.title("🧪 Expert Sélecteur EJS")
st.subheader("Base Intégrale : 500+ Fluides & 17 Familles d'Élastomères")

# --- BASE DE DONNÉES (Structure 17 lignes fixe pour les 17 matières) ---
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
    
    # --- OPTIONS ---
    "SANS CHOIX": [0]*17,

    # --- AGROALIMENTAIRE / HYGIÈNE ---
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 4, 4, 3, 2],
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5, 2, 3, 1, 1],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5, 2, 2, 2, 1],
    "Acide Peracétique": [5, 2, 3, 4, 4, 5, 2, 4, 5, 5, 5, 3, 5, 4, 4, 2, 2],

    # --- CHIMIE ET SOLVANTS ---
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5, 4, 3, 1, 1],
    "Acétone / MEK": [4, 1, 1, 2, 1, 5, 1, 3, 5, 5, 5, 2, 5, 1, 2, 1, 1],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 1, 1, 5],
    "Skydrol LD-4": [5, 1, 1, 1, 1, 1, 1, 2, 5, 5, 5, 2, 5, 1, 5, 1, 5]
    
    # [ACTION] Insérez vos 490 autres fluides ici en suivant exactement ce format :
    # "Nom du Fluide": [X, X, X, X, X, X, X, X, X, X, X, X, X, X, X, X, X],
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
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max"]
    fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    f1 = st.selectbox("Fluide 1", fluides, index=0)
    f2 = st.selectbox("Fluide 2", fluides, index=fluides.index("SANS CHOIX"))
    t_serv = st.slider("Température (°C)", -200, 350, 20)
    
    ref_ejs = st.selectbox("Référence EJS", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs]

# --- LOGIQUE DE TRI (MEILLEURS EN HAUT) ---
df["Score"] = df[f1] + df[f2]
# On trie avant l'affichage pour forcer le classement par performance
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE DES RÉSULTATS ---
st.info(f"Analyse pour : {f1} {'+ ' + f2 if f2 != 'SANS CHOIX' else ''}")

for _, row in df_tri.iterrows():
    is_ref = famille_cible == row["Famille Générique"]
    temp_ok = row["Temp Min"] <= t_serv <= row["Temp Max"]
    seuil_v = 4 if f2 == "SANS CHOIX" else 8
    
    if not temp_ok:
        bg = "rgba(220, 53, 69, 0.7)" # Rouge (Température)
    elif row["Score"] >= seuil_v:
        bg = "rgba(40, 167, 69, 0.7)" # Vert (Meilleure Performance)
    else:
        bg = "rgba(253, 126, 20, 0.7)" # Orange (Moyen)

    border = "6px solid white" if is_ref else "none"

    # Construction HTML sécurisée par morceaux (évite SyntaxError)
    card = '<div style="background-color:' + bg + '; border:' + border + '; border-radius:10px; padding:15px; margin-bottom:10px; color:white;">'
    card += '<div style="display: flex; justify-content: space-between; align-items: center;">'
    card += '<b>' + row["Famille Générique"] + (' (Ref ⭐)' if is_ref else '') + '</b>'
    card += '<span style="background:white; color:black; padding:2px 8px; border-radius:5px; font-weight: bold;">'
    card += 'Score: ' + str(row["Score"]) + ('/5' if f2 == "SANS CHOIX" else '/10') + '</span></div>'
    card += '<hr style="margin:8px 0; border:0; border-top:1px solid white; opacity:0.3;">'
    card += '<small>' + row["Spécificité"] + ' | ' + str(row["Temp Min"]) + '°C à ' + str(row["Temp Max"]) + '°C</small></div>'
    
    st.markdown(card, unsafe_allow_html=True)s
