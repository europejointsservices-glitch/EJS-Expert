import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Expert Élastomères EJS v5.6", layout="wide")

st.title("🧪 Expert Élastomères EJS v5.6")
st.subheader("Sélection par Performance Technique")

# --- BASE DE DONNÉES (Strictement identique à votre première version) ---
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

# --- SIDEBAR (PARAMÈTRES) ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    f1 = st.selectbox("Sélectionner Fluide 1", fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)

# --- CALCUL ET TRI ---
df["Score"] = df[f1] + df[f2]
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE DU TABLEAU DE SYNTHÈSE (C'était le coeur de la v5.6) ---
st.write(f"### 📊 Synthèse Comparative : {f1} + {f2}")
st.dataframe(df_tri)

st.write("---")

# --- AFFICHAGE DES FICHES DRC (Structure v5.6 d'origine) ---
st.write("### 📑 Détails Techniques et DRC")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    # Détermination du statut visuel
    if not temp_ok:
        status_color = "🔴"
        status_text = "HORS TEMPÉRATURE"
    elif row["Score"] >= 8:
        status_color = "🟢"
        status_text = "RECOMMANDÉ"
    else:
        status_color = "🟠"
        status_text = "VIGILANCE / USAGE STATIQUE"

    # Affichage en bloc simple et propre (lisible partout)
    with st.expander(f"{status_color} {row['Compound EJS']} - Score : {row['Score']}/10"):
        st.write(f"**Matière :** {row['Famille']}")
        st.write(f"**Dureté :** {row['Dureté']} | **Couleur :** {row['Couleur']}")
        st.write(f"**Norme :** {row['Norme']}")
        st.write(f"**Résistance chimique :** {f1} ({row[f1]}/5) + {f2} ({row[f2]}/5)")
        st.write(f"**Plage Température :** {row['Temp Min']}°C à {row['Temp Max']}°C")
        st.write(f"**Statut :** {status_text}")
