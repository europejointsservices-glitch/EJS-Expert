import streamlit as st
import pandas as pd

# 1. Configuration de la page (Mode large v5.6)
st.set_page_config(page_title="EJS Expert v9.7", layout="wide")

st.title("🧪 Expert Élastomères EJS v9.7")
st.subheader("Analyse Technique - 100 Fluides & Jus de Saumure")

# --- BASE DE DONNÉES ENRICHIE (Correction des crochets et parenthèses) ---
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
    
    # --- FLUIDES AGROALIMENTAIRES ---
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Vapeur (SEP 140°C)": [5, 1, 2, 2, 3, 2, 4, 5, 3, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    "Eau Potable": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Lait / Produits Laitiers": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    
    # --- CHIMIE & INDUSTRIE (Correction syntaxe image_10da84) ---
    "Acide Chlorhydrique 37%": [5, 1, 5, 5, 5, 5, 5, 5, 2, 2, 5],
    "Acide Sulfurique 98%": [4, 1, 3, 4, 5, 5, 5, 3, 1, 1, 5],
    "Hypochlorite de Soude": [5, 2, 5, 5, 5, 5, 5, 5, 2, 3, 5],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Méthanol": [5, 4, 1, 1, 2, 4, 5, 1, 4, 5, 5],
    "Air Comprimé": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Azote Liquide": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
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

# --- SIDEBAR (Correction parenthèse image_10d9ca) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Filtrer par Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence Commerciale EJS")
    # Correction de la ligne 86 (image_10d9ca)
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- SYNOPSIS ---
st.info(f"🧐 **Analyse EJS v9.7 :** Étude pour **{f1}** et **{f2}**. Validation technique complète.")

# --- SECTION 1 : FICHES (Correction f-string image_0fe223) ---
for index, row in df_tri.iterrows():
    highlight = famille_cible == row["Famille Générique"]
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    if not temp_ok:
        border_color, bg_color = "#dc3545", "rgba(220, 53, 69, 0.7)"
    elif row["Score"] >= 8:
        border_color, bg_color = "#28a745", "rgba(40, 167, 69, 0.7)"
    else:
        border_color, bg_color = "#fd7e14", "rgba(253, 126, 20, 0.7)"

    border_style = "6px solid white" if highlight else f"2px solid {border_color}"

    # Utilisation d'un bloc markdown simple pour éviter les erreurs de triple-guillemets complexes
    content = f"""
    <div style="border: {border_style}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <b style="font-size: 1.4em;">{row['Famille Générique']} {"⭐" if highlight else ""}</b>
            <b style="font-size: 1.2em; color: black; background: white; padding: 4px 12px; border-radius: 8px;">Score : {row['Score']}/10</b>
        </div>
        <hr style="margin: 10px 0; border: 0; border-top: 1px solid white; opacity: 0.5;">
        <p style="margin: 5px 0;"><b>🔍 Notes :</b> {f1} (<b>{row[f1]}/5</b>) + {f2} (<b>{row[f2]}/5</b>)</p>
        <p style="margin: 10px 0 0 0; font-size: 0.95em;">
        <b>Usage :</b> {row['Spécificité']} | <b>Temp :</b> {row['Temp Min']}°C / {row['Temp Max']}°C
        </p>
    </div>
    """
    st.markdown(content, unsafe_allow_html=True)

# --- SECTION 2 : TABLEAU ---
st.write("---")
st.write("### 📊 Synthèse Comparative Complète")
st.dataframe(df_tri.drop(columns=["Qualité DRC"]), use_container_width=True)
