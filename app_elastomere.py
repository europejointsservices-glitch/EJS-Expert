import streamlit as st
import pandas as pd

# 1. Configuration (Mode large v5.6)
st.set_page_config(page_title="EJS Expert v9.2", layout="wide")

st.title("🧪 Expert Élastomères EJS v9.2")
st.subheader("Base 100 Fluides - Nomenclature Générique & Réf. EJS")

# --- BASE DE DONNÉES (Générique) ---
data = {
    "Famille Générique": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Rouge", "Blanc"],
    "Norme": ["FDA/EC1935", "Standard", "Aeronautique", "FDA", "FDA"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    # --- FLUIDES (Identique v9.0) ---
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 5],
    "Soude (NEP 2%)": [5, 4, 2, 3, 5],
    "Acide Nitrique (NEP 1%)": [2, 1, 4, 1, 5],
    "Eau Potable": [5, 5, 5, 5, 5],
    "Graisse Animale": [1, 5, 5, 4, 5],
    "Huile Végétale": [1, 5, 5, 4, 5],
    "Acide Chlorhydrique 37%": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minérale": [1, 5, 5, 2, 5],
    "Gazole / Diesel": [1, 5, 5, 1, 5],
    # ... conservez vos 100 fluides ici
}

# Mapping Références EJS
ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM",
    "EJS-N70": "NBR",
    "EJS-V70ETP": "FKM",
    "EJS-S70": "Silicone",
    "EJS-P70": "PTFE"
}

df = pd.DataFrame(data)

# --- LOGIQUE DRC ---
def evaluer_drc(row):
    if any(x in row["Famille Générique"] for x in ["PTFE", "FKM"]): return "Excellente"
    elif any(x in row["Famille Générique"] for x in ["EPDM", "NBR"]): return "Moyenne"
    else: return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR (Ordre hiérarchique) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # 1. Choix techniques (Primaires)
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    # 2. Filtre DRC (Primaire)
    st.write("---")
    choix_drc = st.multiselect("Filtrer par Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Moyenne"])
    
    # 3. Référence EJS (Secondaire - En bas)
    st.write("---")
    st.subheader("🛒 Référence Commerciale")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- SYNOPSIS ---
st.info(f"🧐 **Analyse EJS :** Étude comparative sur **{f1}** et **{f2}**.")

# --- SECTION 1 : FICHES (TEXTE BLANC) ---
for index, row in df_tri.iterrows():
    # Mise en évidence de la référence EJS choisie
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
            <p style="margin: 5px 0;"><b>🔍 Synopsis des notes chimiques :</b></p>
            <ul style="margin: 5px 0; font-size: 1em;">
                <li>{f1} : <b>{row[f1]}/5</b></li>
                <li>{f2} : <b>{row[f2]}/5</b></li>
            </ul>
            <p style="margin: 15px 0 0 0; font-size: 0.95em;">
            <b>Dureté :</b> {row['Dureté']} | <b>Couleur :</b> {row['Couleur']} | <b>Norme :</b> {row['Norme']}
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- SECTION 2 : TABLEAU (BAS) ---
st.write("---")
st.write("### 📊 Synthèse Comparative Complète")
st.dataframe(df_tri.drop(columns=["Qualité DRC"]), use_container_width=True)
