import streamlit as st
import pandas as pd

# Configuration de la page pour un affichage optimal
st.set_page_config(page_title="EJS Expert v5.7", layout="wide")

# Titre de l'application
st.title("🧪 Expert Élastomères EJS v5.7")
st.subheader("Sélection par Performance Technique")

# --- BASE DE DONNÉES (Identique à la v5.6) ---
data = {
    "Compound EJS": ["EJS-E70P", "EJS-N70", "EJS-V70ETP", "EJS-S70", "EJS-P70"],
    "Famille": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    "Acide Chlorhydrique": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minerale": [1, 5, 5, 2, 5],
    "Vapeur": [5, 1, 2, 3, 5],
    # Ajoutez ici vos 45 fluides sans rien changer...
}

df = pd.DataFrame(data)
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Temp Min", "Temp Max"]]

# --- SIDEBAR (SÉLECTEURS) ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    fluide_1 = st.selectbox("Sélectionner Fluide 1", fluides)
    fluide_2 = st.selectbox("Sélectionner Fluide 2", fluides)
    temp_service = st.slider("Température de service (°C)", -200, 260, 20)

# --- LOGIQUE DE CALCUL ---
df["Score"] = df[fluide_1] + df[fluide_2]
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE ADAPTATIF (EMPILAGE MOBILE) ---
st.write(f"### Résultats pour : {fluide_1} + {fluide_2}")

for index, row in df_tri.iterrows():
    # Vérification température
    temp_ok = row["Temp Min"] <= temp_service <= row["Temp Max"]
    
    # Détermination de la couleur de bordure
    color = "#28a745" if row["Score"] >= 8 and temp_ok else "#fd7e14"
    if not temp_ok: color = "#dc3545" # Rouge si hors température

    # Création d'un bloc visuel (Carte)
    with st.container():
        st.markdown(f"""
        <div style="border: 3px solid {color}; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #f8f9fa;">
            <h4 style="margin:0; color: #333;">{row['Compound EJS']} ({row['Famille']})</h4>
            <p style="margin:5px 0;"><b>Performance : {row['Score']}/10</b> (F1: {row[fluide_1]}/5 | F2: {row[fluide_2]}/5)</p>
            <p style="margin:0; font-size: 0.9em;">Plage : {row['Temp Min']}°C à {row['Temp Max']}°C</p>
        </div>
        """, unsafe_items_allowed=True)
