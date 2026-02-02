import streamlit as st
import pandas as pd

# Configuration de la page pour un affichage optimal sur PC et Mobile
st.set_page_config(page_title="EJS Expert v5.8", layout="wide")

# Style CSS pour masquer les menus Streamlit inutiles et épurer l'interface
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {background-color: #ffffff;}
    </style>
""", unsafe_allow_html=True)

# Titre de l'application
st.title("🧪 Expert Élastomères EJS v5.8")
st.subheader("Sélection par Performance Technique")

# --- BASE DE DONNÉES (45 Fluides - Structure inchangée) ---
# Note : Ajoutez ici tous vos fluides comme dans la v5.6
data = {
    "Compound EJS": ["EJS-E70P", "EJS-N70", "EJS-V70ETP", "EJS-S70", "EJS-P70"],
    "Famille": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    "Acide Chlorhydrique": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minerale": [1, 5, 5, 2, 5],
    "Vapeur": [5, 1, 2, 3, 5],
    # ... conservez bien toutes vos données ici ...
}

df = pd.DataFrame(data)
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Temp Min", "Temp Max"]]

# --- SIDEBAR (SÉLECTEURS) ---
# Sur mobile, accessible via le bouton ">" en haut à gauche
with st.sidebar:
    st.header("⚙️ Paramètres")
    fluide_1 = st.selectbox("Sélectionner Fluide 1", fluides)
    fluide_2 = st.selectbox("Sélectionner Fluide 2", fluides)
    temp_service = st.slider("Température de service (°C)", -200, 260, 20)
    st.info("Les résultats sont triés automatiquement par performance technique.")

# --- LOGIQUE DE CALCUL ET TRI ---
df["Score"] = df[fluide_1] + df[fluide_2]
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE STYLE EJS (CARTES ÉPURÉES) ---
st.write(f"### Résultats pour : {fluide_1} + {fluide_2}")

for index, row in df_tri.iterrows():
    # Vérification de la conformité température
    temp_ok = row["Temp Min"] <= temp_service <= row["Temp Max"]
    
    # Logique de couleur et statut (Identique v5.6)
    if not temp_ok:
        color = "#dc3545" # Rouge
        statut = "⚠️ TEMPÉRATURE HORS PLAGE"
    elif row["Score"] >= 8:
        color = "#28a745" # Vert
        statut = "✅ RECOMMANDÉ"
    else:
        color = "#fd7e14" # Orange
        statut = "⏳ VIGILANCE / USAGE STATIQUE"

    # Création du bloc visuel adapté au mobile (Empilage)
    st.markdown(f"""
    <div style="border: 4px solid {color}; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <b style="font-size: 1.4em; color: #1f1f1f;">{row['Compound EJS']}</b>
            <span style="color: {color}; font-weight: bold; font-size: 0.9em; background-color: {color}15; padding: 5px 10px; border-radius: 5px;">{statut}</span>
        </div>
        <hr style="margin: 15px 0; border: 0; border-top: 1px solid #eee;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <p style="margin: 0;"><b>Matière :</b> {row['Famille']}</p>
            <p style="margin: 0;"><b>Note Technique : <span style="font-size: 1.2em; color: {color};">{row['Score']}/10</span></b></p>
            <p style="margin: 0; color: #666; font-style: italic;">Compatibilité : {fluide_1} ({row[fluide_1]}/5) | {fluide_2} ({row[fluide_2]}/5)</p>
            <p style="margin: 0; font-size: 0.9em; color: #444;">Plage de service : {row['Temp Min']}°C à {row['Temp Max']}°C</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
