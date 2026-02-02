import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="EJS Expert v10.0", layout="wide")

st.title("🧪 Expert Élastomères EJS v10.0")
st.subheader("Base Expert 200 Fluides - Maintenance & Agroalimentaire")

# --- BASE DE DONNÉES ENRICHIE (200 PRODUITS) ---
# Note : Les notes sont basées sur la compatibilité standard EJS (1: Incompatible à 5: Excellent)
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
    
    # --- OPTIONS DE SÉLECTION ---
    "SANS CHOIX": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    
    # --- AGROALIMENTAIRE / NEP / SEP ---
    "Vapeur (SEP 140°C)": [5, 1, 2, 2, 3, 2, 4, 5, 3, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    "Acide Nitrique (NEP)": [2, 1, 4, 4, 5, 4, 5, 4, 2, 1, 5],
    "Eau Potable / Glycolée": [5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Lait / Fromage": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Huiles Végétales": [1, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Vins et Spiritueux": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    
    # --- ACIDES & BASES (SÉLECTION 200) ---
    "Acide Chlorhydrique 37%": [5, 1, 5, 5, 5, 5, 5, 5, 2, 2, 5],
    "Acide Sulfurique 98%": [4, 1, 3, 4, 5, 5, 5, 3, 1, 1, 5],
    "Acide Phosphorique 85%": [5, 2, 5, 5, 5, 5, 5, 5, 3, 2, 5],
    "Soude Caustique 50%": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    "Eau de Javel (Hypochlorite)": [5, 2, 5, 5, 5, 5, 5, 5, 2, 3, 5],
    "Ammoniaque": [5, 4, 1, 1, 1, 1, 4, 5, 4, 4, 5],
    "Potasse": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    
    # --- HYDROCARBURES & SOLVANTS ---
    "Gazole / Diesel / Fuel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Essence Sans Plomb": [1, 3, 5, 5, 5, 5, 5, 5, 4, 1, 5],
    "Kérosène (Jet A1)": [1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
    "Huile Hydraulique Minérale": [1, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5],
    "Skydrol (Huile Phosphate)": [5, 1, 1, 1, 1, 1, 5, 2, 1, 2, 5],
    "Méthanol / Éthanol": [5, 4, 1, 1, 2, 4, 5, 1, 4, 5, 5],
    "Acétone / MEK": [4, 1, 1, 1, 1, 1, 5, 3, 1, 2, 5],
    "Toluène / Benzène": [1, 1, 5, 5, 5, 5, 5, 5, 2, 1, 5],
    "Trichloroéthylène": [1, 1, 5, 5, 5, 5, 5, 5, 1, 1, 5],
    
    # --- GAZ & DIVERS ---
    "Air Comprimé": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Oxygène": [4, 2, 5, 5, 5, 5, 5, 4, 2, 4, 5],
    "Azote Gazeux / Liquide": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Gaz Naturel (Méthane)": [1, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5],
    "Propane / Butane": [1, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5],
    "Eau de Mer": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
}

# Mapping Références Europe Joints Services (Strictement v9.9.2)
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

# --- SIDEBAR (Sélecteurs v9.9.2) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    cols_tech = ["Famille Générique", "Dureté", "Couleur", "Spécificité", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = sorted([c for c in df.columns if c not in cols_tech])
    
    idx_sans_choix = liste_fluides.index("SANS CHOIX")
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides, index=0)
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
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- SECTION AFFICHAGE (Cartes Transparentes Texte Blanc) ---
info_text = f"Analyse pour **{f1}**" if f2 == "SANS CHOIX" else f"Analyse pour **{f1}** et **{f2}**"
st.info(f"🧐 {info_text}.")

for index, row in df_tri.iterrows():
    highlight = famille_cible == row["Famille Générique"]
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    # Définition des couleurs (RGBA 70%)
    if not temp_ok:
        border_color, bg_color = "#dc3545", "rgba(220, 53, 69, 0.7)"
    elif row["Score"] >= (4 if f2 == "SANS CHOIX" else 8):
        border_color, bg_color = "#28a745", "rgba(40, 167, 69, 0.7)"
    else:
        border_color, bg_color = "#fd7e14", "rgba(253, 126, 20, 0.7)"

    border_style = "6px solid white" if highlight else f"2px solid {border_color}"

    st.markdown(f"""
        <div style="border: {border_style}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 1.4em; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">{row['Famille Générique']} {"⭐" if highlight else ""}</b>
                <b style="font-size: 1.2em; color: black; background: white; padding: 4px 12px; border-radius: 8px;">
                    Score : {row['Score']}/{'5' if f2 == 'SANS CHOIX' else '10'}
                </b>
            </div>
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid white; opacity: 0.5;">
            <p style="margin: 5px 0;"><b>🔍 Synopsis :</b> {f1} ({row[f1]}/5) {f' + {f2} ({row[f2]}/5)' if f2 != 'SANS CHOIX' else ''}</p>
            <p style="margin: 10px 0 0 0; font-size: 0.95em;">
            <b>Spécificité :</b> {row['Spécificité']} | <b>Temp :</b> {row['Temp Min']}°C / {row['Temp Max']}°C
            </p>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.write("### 📊 Synthèse Comparative (Base 200)")
st.dataframe(df_tri.drop(columns=["Qualité DRC", "SANS CHOIX"]), use_container_width=True)
