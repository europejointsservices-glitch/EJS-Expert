import streamlit as st
import pandas as pd

# 1. Configuration Large (Comme sur PC)
st.set_page_config(page_title="EJS Expert v6.2", layout="wide")

# 2. Style Sombre Pro (Fond noir, texte blanc)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1A1C24; }
    .stDataFrame { background-color: #1A1C24; }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Expert Élastomères EJS v6.2")
st.write("---")

# 3. VOTRE BASE DE DONNÉES COMPLÈTE (Structure v5.6)
data = {
    "Compound EJS": ["EJS-E70P", "EJS-N70", "EJS-V70ETP", "EJS-S70", "EJS-P70"],
    "Famille": ["EPDM", "NBR", "FKM", "Silicone", "PTFE"],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Rouge", "Blanc"],
    "Temp Min": [-50, -30, -20, -60, -200],
    "Temp Max": [150, 100, 200, 200, 260],
    "Acide Chlorhydrique": [5, 1, 5, 2, 5],
    "Soude Caustique": [5, 4, 2, 3, 5],
    "Huile Minerale": [1, 5, 5, 2, 5],
    "Vapeur": [5, 1, 2, 3, 5],
    # Remettez ici l'intégralité de vos 45 fluides
}

df = pd.DataFrame(data)
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Dureté", "Couleur", "Temp Min", "Temp Max"]]

# 4. SIDEBAR (Paramètres)
with st.sidebar:
    st.header("⚙️ Configuration")
    f1 = st.selectbox("Sélectionner Fluide 1", fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    st.write("---")
    vue_mobile = st.checkbox("Activer l'affichage par cartes (Mobile)", value=False)

# 5. CALCULS (Somme des notes)
df["Score"] = df[f1] + df[f2]
df_tri = df.sort_values(by="Score", ascending=False)

# 6. AFFICHAGE DU TABLEAU RÉCAPITULATIF (Votre structure préférée)
st.write(f"### 📊 Synthèse Comparative : {f1} + {f2}")
st.dataframe(df_tri, use_container_width=True)

# 7. AFFICHAGE OPTIONNEL PAR CARTES (Pour le terrain)
if vue_mobile:
    st.write("---")
    st.write("### 📑 Détails par Compound")
    for index, row in df_tri.iterrows():
        temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
        color = "#00FF7F" if row["Score"] >= 8 and temp_ok else "#FFA500"
        if not temp_ok: color = "#FF4B4B"

        st.markdown(f"""
        <div style="border: 2px solid {color}; border-radius: 8px; padding: 15px; margin-bottom: 10px; background-color: #1A1C24;">
            <b style="font-size: 1.2em;">{row['Compound EJS']} ({row['Famille']})</b><br>
            <span>Dureté: {row['Dureté']} | Couleur: {row['Couleur']}</span><br>
            <span style="color:{color}; font-weight:bold;">Note Globale: {row['Score']}/10</span><br>
            <span style="font-size: 0.8em; color: #BBB;">Plage: {row['Temp Min']}°C à {row['Temp Max']}°C</span>
        </div>
        """, unsafe_allow_html=True)
