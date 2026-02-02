import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Expert Sélecteur EJS", layout="wide")

# Titre Simple
st.title("🧪 Expert Sélecteur EJS")
st.subheader("Base expert 500 Fluides")

# --- BASE DE DONNÉES (17 lignes strictes) ---
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
    
    # --- FLUIDES (STRUCTURE 17 VALEURS) ---
    "SANS CHOIX": [0]*17,
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 4, 4, 3, 2],
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5, 2, 3, 1, 1],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5, 2, 2, 2, 1],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 1, 1, 5],
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5, 4, 3, 1, 1]
}

# Mapping Commercial EJS
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM", "EJS-N70": "NBR", "EJS-V70": "Viton™ A",
    "EJS-V75GF": "Viton™ GF-S", "EJS-V75GFLT": "Viton™ GFLT-S",
    "EJS-V75ETP": "Viton™ Extreme ETP", "EJS-AF80": "AFLAS (FEPM)",
    "EJS-K75CH": "FFKM (Chimie Std)", "EJS-K75AL": "FFKM (Alimentaire/Vapeur)",
    "EJS-K80HT": "FFKM (Haute Temp)", "EJS-H70": "HNBR", "EJS-S70": "Silicone (VMQ)", 
    "EJS-P70": "PTFE", "EJS-FS70": "Fluorosilicone (FMVQ)", 
    "EJS-PS70": "Silicone Phénylé (PMVQ)", # C'est ICI qu'il apparaitra
    "EJS-NR65": "Caoutchouc Naturel (NR)", "EJS-AU90": "Polyuréthane (AU)"
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
    st.header("⚙️ Filtres")
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    f1 = st.selectbox("Fluide 1", liste_fluides, index=0)
    f2 = st.selectbox("Fluide 2", liste_fluides, index=liste_fluides.index("SANS CHOIX"))
    t_serv = st.slider("Température (°C)", -200, 350, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence EJS")
    ref_ejs = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs]

# --- CALCULS ET TRI CRUCIAL ---
df["Score"] = df[f1] + df[f2]
# LE TRI PAR SCORE DESCENDANT (Les VERTS en haut)
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- AFFICHAGE ---
st.info(f"Analyse : {f1} {'+ ' + f2 if f2 != 'SANS CHOIX' else ''}")

for _, row in df_tri.iterrows():
    is_ref = famille_cible == row["Famille Générique"]
    temp_ok = row["Temp Min"] <= t_serv <= row["Temp Max"]
    seuil = 4 if f2 == "SANS CHOIX" else 8
    
    if not temp_ok:
        b_col, bg_col = "#dc3545", "rgba(220, 53, 69, 0.7)" # ROUGE
    elif row["Score"] >= seuil:
        b_col, bg_col = "#28a745", "rgba(40, 167, 69, 0.7)" # VERT
    else:
        b_col, bg_col = "#fd7e14", "rgba(253, 126, 20, 0.7)" # ORANGE

    b_style = "6px solid white" if is_ref else f"2px solid {b_col}"

    html = f"""
    <div style="border: {b_style}; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: {bg_col}; color: white;">
        <div style="display: flex; justify-content: space-between;">
            <b>{row['Famille Générique']} {'⭐' if is_ref else ''}</b>
            <span style="background: white; color: black; padding: 2px 8px; border-radius: 5px;">Score: {row['Score']}</span>
        </div>
        <div style="font-size: 0.85em; margin-top: 5px;">
            {row['Spécificité']} | {row['Temp Min']}°C à {row['Temp Max']}°C
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

st.write("---")
st.dataframe(df_tri.drop(columns=["Qualité DRC", "SANS CHOIX"]))
