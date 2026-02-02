import streamlit as st
import pandas as pd

# 1. Configuration
st.set_page_config(page_title="EJS Expert v6.1", layout="wide")

# 2. Style Sombre Intégral
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1A1C24; }
    .stDataFrame { background-color: #1A1C24; }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Expert Élastomères EJS v6.1")
st.subheader("Mode Sombre Pro - Expertise DRC Incluse")

# 3. BASE DE DONNÉES (Structure enrichie avec DRC)
data = {
    "Compound EJS": ["EJS-E70P", "EJS-N70", "EJS-V70ETP", "EJS-S70", "EJS-P70"],
    "Famille": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Rouge", "Blanc"],
    "Norme": ["FDA/EC1935", "Standard", "Aeronautique", "FDA", "FDA"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    "Acide Chlorhydrique": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minerale": [1, 5, 5, 2, 5],
    "Vapeur": [5, 1, 2, 3, 5],
}

df = pd.DataFrame(data)
# Liste des fluides pour les sélecteurs
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max"]]

# 4. Paramètres (Sidebar)
with st.sidebar:
    st.header("⚙️ Paramètres")
    f1 = st.selectbox("Sélectionner Fluide 1", fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", fluides)
    t_service = st.slider("Température (°C)", -200, 260, 20)
    st.markdown("---")
    st.write("Expertise Europe Joints Services")

# 5. Calcul et Tri
df["Score"] = df[f1] + df[f2]
df_tri = df.sort_values(by="Score", ascending=False)

# 6. TABLEAU RÉCAPITULATIF (Vision globale)
st.write("### 📊 Tableau de synthèse")
# On affiche les colonnes principales pour le tableau
cols_tab = ["Compound EJS", "Famille", "Dureté", "Couleur", "Score", "Temp Min", "Temp Max"]
st.dataframe(df_tri[cols_tab], use_container_width=True)

# 7. AFFICHAGE DES CARTES (Détails DRC + Mobile)
st.write(f"### 📑 Fiches détaillées : {f1} + {f2}")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    if not temp_ok:
        color, statut = "#FF4B4B", "⚠️ HORS TEMP"
    elif row["Score"] >= 8:
        color, statut = "#00FF7F", "✅ RECOMMANDÉ"
    else:
        color, statut = "#FFA500", "⏳ VIGILANCE"

    card_html = f"""
    <div style="border: 2px solid {color}; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: #1A1C24;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <b style="font-size: 1.4em; color: white;">{row['Compound EJS']}</b>
            <span style="color: {color}; font-weight: bold; border: 1px solid {color}; padding: 3px 10px; border-radius: 5px;">{statut}</span>
        </div>
        <hr style="margin: 15px 0; border: 0; border-top: 1px solid #333;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;">
            <div><b>Matière :</b> {row['Famille']}</div>
            <div><b>Dureté :</b> {row['Dureté']}</div>
            <div><b>Couleur :</b> {row['Couleur']}</div>
            <div><b>Norme :</b> {row['Norme']}</div>
        </div>
        <div style="margin-top: 15px;">
            <p style="margin: 0;"><b>Note Technique : <span style="font-size: 1.2em; color: {color};">{row['Score']}/10</span></b></p>
            <p style="margin: 5px 0 0 0; color: #BBB; font-size: 0.85em;">Plage : {row['Temp Min']}°C à {row['Temp Max']}°C</p>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
