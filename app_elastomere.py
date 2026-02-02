import streamlit as st
import pandas as pd

# Configuration pour un affichage large et moderne
st.set_page_config(page_title="EJS Expert v5.9", layout="wide")

# STYLE CSS : Fond gris clair pour faire ressortir les cartes blanches
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Titre de l'application
st.title("🧪 Expert Élastomères EJS v5.9")
st.subheader("Sélection par Performance Technique")

# --- BASE DE DONNÉES (Identique v5.6 - À compléter avec vos 45 fluides) ---
data = {
    "Compound EJS": ["EJS-E70P", "EJS-N70", "EJS-V70ETP", "EJS-S70", "EJS-P70"],
    "Famille": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    "Acide Chlorhydrique": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minerale": [1, 5, 5, 2, 5],
    "Vapeur": [5, 1, 2, 3, 5],
}

df = pd.DataFrame(data)
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Temp Min", "Temp Max"]]

# --- SIDEBAR (SÉLECTEURS) ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    fluide_1 = st.selectbox("Sélectionner Fluide 1", fluides)
    fluide_2 = st.selectbox("Sélectionner Fluide 2", fluides)
    temp_service = st.slider("Température de service (°C)", -200, 260, 20)
    st.markdown("---")
    st.info("Les résultats sont triés par performance technique décroissante.")

# --- LOGIQUE DE CALCUL ---
df["Score"] = df[fluide_1] + df[fluide_2]
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE DES FICHES EJS ---
st.write(f"### Résultats pour : {fluide_1} + {fluide_2}")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= temp_service <= row["Temp Max"]
    
    # Couleurs et statuts officiels EJS
    if not temp_ok:
        color = "#dc3545" # Rouge
        statut = "⚠️ HORS TEMPÉRATURE"
    elif row["Score"] >= 8:
        color = "#28a745" # Vert
        statut = "✅ RECOMMANDÉ"
    else:
        color = "#fd7e14" # Orange
        statut = "⏳ VIGILANCE / STATIQUE"

    # Création de la carte avec ombre pour le relief
    st.markdown(f"""
    <div style="border: 4px solid {color}; border-radius: 12px; padding: 20px; margin-bottom: 20px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <b style="font-size: 1.4em; color: #1a1a1a;">{row['Compound EJS']}</b>
            <span style="border: 2px solid {color}; color: {color}; font-weight: bold; font-size: 0.8em; padding: 4px 12px; border-radius: 20px; background-color: white;">
                {statut}
            </span>
        </div>
        <hr style="margin: 15px 0; border: 0; border-top: 1px solid #eee;">
        <div style="line-height: 1.6;">
            <p style="margin: 0;"><b>Famille :</b> {row['Famille']}</p>
            <p style="margin: 0;"><b>Note Globale : <span style="font-size: 1.2em; color: {color};">{row['Score']}/10</span></b></p>
            <p style="margin: 0; font-size: 0.9em; color: #555;">Détail : {fluide_1} ({row[fluide_1]}/5) | {fluide_2} ({row[fluide_2]}/5)</p>
            <p style="margin: 0; font-size: 0.9em; color: #555;">Plage : {row['Temp Min']}°C à {row['Temp Max']}°C</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
