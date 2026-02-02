import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="EJS Expert v9.9.2", layout="wide")

# Titre épuré (v9.9.1 maintenue)
st.title("🧪 Expert Élastomères EJS v9.9.2")
st.subheader("Base Expert 100+ Fluides - Spécialités")

# --- BASE DE DONNÉES V9.9.1 ---
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
    
    # Option Neutre pour le calcul
    "SANS CHOIX": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    
    # Fluides (Base 9.9.1 complète)
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Acide Chlorhydrique 37%": [5, 1, 5, 5, 5, 5, 5, 5, 2, 2, 5],
    "Acide Sulfurique 98%": [4, 1, 3, 4, 5, 5, 5, 3, 1, 1, 5],
    "Vapeur (SEP 140°C)": [5, 1, 2, 2, 3, 2, 4, 5, 3, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    "Eau Potable": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Méthanol": [5, 4, 1, 1, 2, 4, 5, 1, 4, 5, 5],
    "Huile Hydraulique": [1, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5],
    "Lait / Produits Laitiers": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
}

ejs_refs = {
    "AUCUNE SÉLECTION": None,
    "EJS-E70P": "EPDM", "EJS-N70": "NBR", "EJS-V70": "Viton™ A (Standard)",
    "EJS-V75GBL": "Viton™ GBL-S", "EJS-V75GF": "Viton™ GF-S",
    "EJS-V75GFLT": "Viton™ GFLT-S", "EJS-V75ETP": "Viton™ Extreme ETP",
    "EJS-AF80": "AFLAS (FEPM)", "EJS-H70": "HNBR", "EJS-S70": "Silicone", "EJS-P70": "PTFE"
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
    
    # Recherche de l'index de "SANS CHOIX" pour le mettre par défaut
    idx_sans_choix = liste_fluides.index("SANS CHOIX")
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides, index=0)
    # LE DEUXIEME SELECTEUR EST SUR "SANS CHOIX" PAR DEFAUT
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides, index=idx_sans_choix)
    
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Filtrer par Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne"])
    
    st.write("---")
    st.subheader("🛒 Référence Commerciale EJS")
    ref_ejs_choisie = st.selectbox("Référence Europe Joints Services", list(ejs_refs.keys()))
    famille_cible = ejs_refs[ref_ejs_choisie]

# --- CALCULS ---
df["Score"] = df[f1] + df[f2]
# Si f2 est "SANS CHOIX", on double la note de f1 pour rester sur une base /10 ou on laisse tel quel ? 
# Ici, le score sera sur 5 si un seul fluide est choisi.
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- SECTION AFFICHAGE ---
info_text = f"Analyse pour **{f1}**" if f2 == "SANS CHOIX" else f"Analyse pour **{f1}** et **{f2}**"
st.info(f"🧐 {info_text}.")

for index, row in df_tri.iterrows():
    highlight = famille_cible == row["Famille Générique"]
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    if not temp_ok:
        border_color, bg_color = "#dc3545", "rgba(220, 53, 69, 0.7)"
    elif row["Score"] >= 4: # Score ajusté si un seul fluide (max 5)
        border_color, bg_color = "#28a745", "rgba(40, 167, 69, 0.7)"
    else:
        border_color, bg_color = "#fd7e14", "rgba(253, 126, 20, 0.7)"

    border_style = "6px solid white" if highlight else f"2px solid {border_color}"

    st.markdown(f"""
        <div style="border: {border_style}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 1.4em;">{row['Famille Générique']}</b>
                <b style="font-size: 1.2em; color: black; background: white; padding: 4px 12px; border-radius: 8px;">Note : {row['Score']}/{'5' if f2 == 'SANS CHOIX' else '10'}</b>
            </div>
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid white; opacity: 0.5;">
            <p style="margin: 10px 0 0 0; font-size: 0.95em;">
            <b>Usage :</b> {row['Spécificité']} | <b>Temp :</b> {row['Temp Min']}°C / {row['Temp Max']}°C
            </p>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.dataframe(df_tri.drop(columns=["Qualité DRC", "SANS CHOIX"]), use_container_width=True)
