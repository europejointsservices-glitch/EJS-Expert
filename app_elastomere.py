import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Expert Élastomères EJS v5.6", layout="wide")

st.title("🧪 Expert Élastomères EJS v5.6")
st.subheader("Sélection par Performance Technique")

# --- BASE DE DONNÉES (Structure exacte v5.6) ---
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
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max"]]

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    f1 = st.selectbox("Sélectionner Fluide 1", fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)

# --- CALCUL ET TRI ---
df["Score"] = df[f1] + df[f2]
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE PAR COLONNES (Le visuel de la 1ère publication) ---
st.write(f"### Expertise pour : {f1} + {f2}")

# On utilise st.columns pour l'affichage côte à côte
cols = st.columns(len(df_tri))

for i, (index, row) in enumerate(df_tri.iterrows()):
    with cols[i]:
        # Logique de couleur des bordures
        temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
        if not temp_ok:
            color = "red"
        elif row["Score"] >= 8:
            color = "green"
        else:
            color = "orange"
        
        # Le container avec la bordure de couleur
        with st.container():
            st.markdown(f"""
                <div style="border: 3px solid {color}; border-radius: 10px; padding: 10px; background-color: white;">
                    <h3 style="text-align: center; color: black;">{row['Compound EJS']}</h3>
                    <p style="text-align: center; color: black;"><b>{row['Famille']}</b></p>
                    <hr>
                    <p style="color: black;"><b>Score : {row['Score']}/10</b></p>
                    <p style="color: black; font-size: 0.8em;">Dureté : {row['Dureté']}<br>
                    Couleur : {row['Couleur']}<br>
                    Norme : {row['Norme']}</p>
                    <p style="color: black; font-size: 0.8em; font-style: italic;">
                    Limites : {row['Temp Min']}°C / {row['Temp Max']}°C</p>
                </div>
            """, unsafe_allow_html=True)

# --- TABLEAU RÉCAPITULATIF (En bas de page) ---
st.write("---")
st.write("### 📊 Tableau de synthèse complet")
st.dataframe(df_tri)
