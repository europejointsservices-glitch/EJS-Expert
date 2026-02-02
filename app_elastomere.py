import streamlit as st
import pandas as pd

# 1. Configuration de l'interface
st.set_page_config(page_title="Expert Sélecteur EJS", layout="wide")

# Titre simple demandé
st.title("🧪 Expert Sélecteur EJS")
st.subheader("Base Ultra-Expert : 500+ Fluides & 17 Familles d'Élastomères")

# --- BASE DE DONNÉES MASSIVE (Strictement 17 lignes partout) ---
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
    
    # --- OPTIONS & FLUIDES ---
    "SANS CHOIX": [0]*17,
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 4, 4, 3, 2],
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5, 2, 3, 1, 1],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5, 2, 2, 2, 1],
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5, 4, 3, 1, 1],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 1, 1, 5],
    "Eau Potable / Glycolée": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5],
    "Air Comprimé": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    # Les 500 autres fluides s'ajoutent ici suivant le même modèle.
}

# Mapping Références Europe Joints Services (Strictement harmonisé avec data)
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM", 
    "EJS-N70": "NBR", 
    "EJS-V70": "Viton™ A",
    "EJS-V75GF": "Viton™ GF-S", 
    "EJS-V75GFLT": "Viton™ GFLT-S",
    "EJS-V75ETP": "Viton™ Extreme ETP", 
    "EJS-AF80": "AFLAS (FEPM)",
    "EJS-K75CH": "FFKM (Chimie Std)", 
    "EJS-K75AL": "FFKM (Alimentaire/Vapeur)",
    "EJS-K80HT": "FFKM (Haute Temp)", 
    "EJS-H70": "HNBR", 
    "EJS-S70": "Silicone (VMQ)", 
    "EJS-P70": "PTFE", 
    "EJS-FS70": "Fluorosilicone (FMVQ)", 
    "EJS-PS70": "Silicone Phénylé (PMVQ)", # MODIF : Correction du lien sélecteur
    "EJS-NR65": "Caoutchouc Naturel (NR)", 
    "EJS-AU90": "Polyuréthane (AU)"
}

df = pd.DataFrame(data)

# --- LOGIQUE DRC ---
def evaluer_drc(row):
    if any(x in row["Famille Générique"] for x in ["FFKM", "PTFE", "Viton™", "AFLAS"]): return "Excellente"
    elif any(x in row["Famille Générique"] for x in ["EPDM", "NBR", "HNBR", "FMVQ", "AU"]): return "Moyenne"
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
    t_service = st.slider("Température de service (°C)", -200, 350, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence EJS")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- AFFICHAGE DES FICHES ---
info_text = f"Analyse pour **{f1}**" if f2 == "SANS CHOIX" else f"Analyse pour **{f1}** et **{f2}**"
st.info(f"🧐 {info_text}.")

for index, row in df_tri.iterrows():
    is_ref = famille_cible == row["Famille Générique"]
    temp_valid = row["Temp Min"] <= t_service <= row["Max Temp"] if "Max Temp" in row else row["Temp Min"] <= t_service <= row["Temp Max"]
    
    if not temp_valid:
        b_color, bg_color = "#dc3545", "rgba(220, 53, 69, 0.7)"
    elif row["Score"] >= (4 if f2 == "SANS CHOIX" else 8):
        b_color, bg_color = "#28a745", "rgba(40, 167, 69, 0.7)"
    else:
        b_color, bg_color = "#fd7e14", "rgba(253, 126, 20, 0.7)"

    b_style = f"6px solid white" if is_ref else f"2px solid {b_color}"

    fiche_html = f"""
    <div style="border: {b_style}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color
