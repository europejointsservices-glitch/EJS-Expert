import streamlit as st
import pandas as pd

# Configuration Dark Mode Native
st.set_page_config(page_title="EJS Expert v6.0", layout="wide")

# STYLE CSS : Mode Sombre intégral et cartes contrastées
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    [data-testid="stSidebar"] {
        background-color: #1A1C24;
    }
    .stSelectbox label, .stSlider label {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Titre de l'application
st.title("🧪 Expert Élastomères EJS v6.0")
st.subheader("Sélection par Performance Technique (Dark Mode)")

# --- BASE DE DONNÉES (Données 100% identiques à votre version d'origine) ---
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
    st.write("Expertise Europe Joints Services")

# --- LOGIQUE DE CALCUL ---
df["Score"] = df[fluide_1] + df[fluide_2]
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE DES FICHES EJS ---
st.write(f"### Résultats pour : {fluide_1} + {fluide_2}")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= temp_service <= row["Temp Max"]
    
    # Couleurs EJS sur fond sombre
    if not temp_ok:
        color = "#FF4B4B" # Rouge vif
        statut = "⚠️ HORS TEMPÉRATURE"
    elif row["Score"] >= 8:
        color = "#00FF7F" # Vert Spring (très visible sur noir)
        statut = "✅ RECOMMANDÉ"
    else:
        color = "#FFA500" # Orange vif
        statut = "⏳ VIGILANCE"

    # Carte style "Tableau de bord"
    st.markdown(f"""
    <div style="border: 2px solid {color}; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: #1A1C24; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <b style="font-size: 1.3em;">{row['Compound EJS']}</b>
            <span style="color: {color}; font-weight: bold; border: 1px solid {color}; padding: 3px 10px; border-radius: 5px;
