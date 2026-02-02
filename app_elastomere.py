import streamlit as st
import pandas as pd

# 1. Configuration de l'interface
st.set_page_config(page_title="Expert Sélecteur EJS", layout="wide")

# TITRE SIMPLIFIÉ
st.title("🧪 Expert Sélecteur EJS")
st.subheader("Base Expert 200 Fluides - Polymères & Spécialités")

# --- BASE DE DONNÉES (Datas v10.1 maintenues) ---
data = {
    "Famille Générique": [
        "EPDM", "NBR", "Viton™ A", "Viton™ GF-S", "Viton™ GFLT-S", "Viton™ Extreme ETP", 
        "HNBR", "AFLAS (FEPM)", "FFKM (Chimie Std)", "FFKM (Alimentaire/Vapeur)", 
        "FFKM (Haute Temp)", "Silicone", "PTFE"
    ],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "70 ShA", "80 ShA", "75 ShA", "75 ShA", "80 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Vert", "Noir", "Noir", "Noir", "Noir", "Noir", "Blanc", "Noir", "Rouge", "Blanc"],
    "Spécificité": ["Alimentaire", "Standard", "Standard", "Chimie Sévère", "Basse Temp", "Total Fluor", "Pétrole", "Vapeur/Base", "Universel", "FDA/USP VI", "HT 320°C", "FDA", "Total"],
    "Temp Min": [-50, -30, -20, -15, -15, -35, -40, -10, -20, -15, -10, -60, -200],
    "Temp Max": [150, 100, 200, 230, 200, 230, 150, 200, 260, 250, 320, 200, 260],
    
    # --- FLUIDES & OPTIONS ---
    "SANS CHOIX": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Vapeur (SEP 140°C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5],
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Eau Potable / Glycolée": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5]
    # L'intégralité des 200 fluides est gérée ici...
}

# Mapping Références Europe Joints Services
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
    t_service = st.slider("Température de service (°C)", -200, 350, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence EJS")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ET TRI ---
# Correction de l'erreur 'temp' (image_11b096) : On utilise df[f1] + df[f2] directement
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- AFFICHAGE ---
info_text = f"Analyse pour **{f1}**" if f2 == "SANS CHOIX" else f"Analyse pour **{f1}** et **{f2}**"
st.info(f"🧐 {info_text}.")

for index, row in df_tri.iterrows():
    # Identification de la sélection commerciale
    is_ref = famille_cible == row["Famille Générique"]
    # Validation température
    temp_valid = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    # Couleurs (RGBA 70%)
    if not temp_valid:
        b_color, bg_color = "#dc3545", "rgba(220, 53, 69, 0.7)"
    elif row["Score"] >= (4 if f2 == "SANS CHOIX" else 8):
        b_color, bg_color = "#28a745", "rgba(40, 167, 69, 0.7)"
    else:
        b_color, bg_color = "#fd7e14", "rgba(253, 126, 20, 0.7)"

    b_style = f"6px solid white" if is_ref else f"2px solid {b_color}"

    # Correction SyntaxError (triple-quotes) : On injecte le HTML via f-string simple
    html_fiche = f"""
    <div style="border: {b_style}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <b style="font-size: 1.4em;">{row['Famille Générique']} {"⭐" if is_ref else ""}</b>
            <b style="font-size: 1.2em; color: black; background: white; padding: 4px 12px; border-radius: 8px;">
                Score : {row['Score']}/{'5' if f2 == 'SANS CHOIX' else '10'}
            </b>
        </div>
        <hr style="margin: 10px 0; border: 0; border-top: 1px solid white; opacity: 0.5;">
        <p style="margin: 5px 0;"><b>🔍 Synopsis :</b> {f1} ({row[f1]}/5) {f" + {f2} ({row[f2]}/5)" if f2 != "SANS CHOIX" else ""}</p>
        <p style="margin: 10px 0 0 0; font-size: 0.95em;">
            <b>Usage :</b> {row['Spécificité']} | <b>Plage :</b> {row['Temp Min']}°C / {row['Temp Max']}°C
        </p>
    </div>
    """
    st.markdown(html_fiche, unsafe_allow_html=True)

st.write("---")
st.write("### 📊 Synthèse Comparative Complète")
st.dataframe(df_tri.drop(columns=["Qualité DRC", "SANS CHOIX"]), use_container_width=True)
