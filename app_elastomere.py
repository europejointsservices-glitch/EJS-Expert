import streamlit as st
import pandas as pd

# 1. Configuration (Mode large v5.6)
st.set_page_config(page_title="EJS Expert v9.3", layout="wide")

st.title("🧪 Expert Élastomères EJS v9.3")
st.subheader("Base 100 Fluides - Élastomères de Spécialités & Réf. EJS")

# --- BASE DE DONNÉES ENRICHIE (Nomenclature Technique) ---
data = {
    "Famille Générique": [
        "EPDM", "NBR", "FKM (Standard)", "FKM (Spécialité GF/ETP)", 
        "HNBR", "AFLAS (FEPM)", "Silicone", "PTFE"
    ],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "70 ShA", "80 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Vert/Brun", "Noir", "Noir", "Rouge", "Blanc"],
    "Norme": ["FDA/EC1935", "Standard", "Standard", "Chimie Sévère", "Pétrole", "Vapeur/Base", "FDA", "FDA"],
    "Temp Min": [-50, -30, -20, -15, -40, -10, -60, -200],
    "Temp Max": [150, 100, 200, 230, 150, 200, 200, 260],
    # --- FLUIDES (Exemple d'application pour les spécialités) ---
    "Vapeur (SEP 140°C)": [5, 1, 2, 4, 3, 5, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 3, 4, 5, 2, 5],
    "Acide Nitrique (NEP 1%)": [2, 1, 4, 5, 2, 4, 1, 5],
    "Eau Potable": [5, 5, 5, 5, 5, 5, 5, 5],
    "Graisse Animale": [1, 5, 5, 5, 5, 4, 4, 5],
    "Huile Végétale": [1, 5, 5, 5, 5, 5, 4, 5],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 1, 5],
    "Huile Hydraulique": [1, 5, 5, 5, 5, 5, 2, 5],
    "Acide Chlorhydrique 37%": [5, 1, 5, 5, 2, 5, 2, 5],
    "Soude Caustique": [5, 4, 1, 3, 4, 5, 2, 5],
    # ... conservez vos 100 fluides ici avec 8 notes au lieu de 5
}

# Mapping Références EJS (Mis à jour avec les spécialités)
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P (EPDM)": "EPDM",
    "EJS-N70 (NBR)": "NBR",
    "EJS-V70 (FKM Std)": "FKM (Standard)",
    "EJS-V75GF (FKM Spé)": "FKM (Spécialité GF/ETP)",
    "EJS-H70 (HNBR)": "HNBR",
    "EJS-AF80 (AFLAS)": "AFLAS (FEPM)",
    "EJS-S70 (Silicone)": "Silicone",
    "EJS-P70 (PTFE)": "PTFE"
}

df = pd.DataFrame(data)

# --- LOGIQUE DRC (Enrichie pour les spécialités) ---
def evaluer_drc(row):
    # Les spécialités comme AFLAS ou FKM GF sont classées en Excellence
    if any(x in row["Famille Générique"] for x in ["PTFE", "FKM", "AFLAS"]): return "Excellente"
    elif any(x in row["Famille Générique"] for x in ["EPDM", "NBR", "HNBR"]): return "Moyenne"
    else: return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR (Hiérarchie EJS) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Filtrer par Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence Commerciale")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- SYNOPSIS ---
st.info(f"🧐 **Analyse EJS v9.3 :** Expertise incluant les élastomères de spécialités pour conditions extrêmes.")

# --- SECTION 1 : FICHES (TEXTE BLANC) ---
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

    st.markdown(f"""
        <div style="border: {border_style}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 1.4em;">{row['Famille Générique']} {"⭐ (VOTRE RÉFÉRENCE)" if highlight else ""}</b>
                <b style="font-size: 1.2em; color: black; background: white; padding: 4px 12px; border-radius: 8px;">Score : {row['Score']}/10</b>
            </div>
            <hr style="margin: 15px 0; border: 0; border-top: 1px solid white; opacity: 0.5;">
            <p style="margin: 5px 0;"><b>🔍 Synopsis des notes chimiques :</b> {f1} (<b>{row[f1]}/5</b>) + {f2} (<b>{row[f2]}/5</b>)</p>
            <p style="margin: 10px 0 0 0; font-size: 0.95em;">
            <b>Spécificité :</b> {row['Norme']} | <b>Dureté :</b> {row['Dureté']} | <b>Plage :</b> {row['Temp Min']}°C / {row['Temp Max']}°C
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- SECTION 2 : TABLEAU ---
st.write("---")
st.write("### 📊 Synthèse Comparative Complète (Spécialités incluses)")
st.dataframe(df_tri.drop(columns=["Qualité DRC"]), use_container_width=True)
