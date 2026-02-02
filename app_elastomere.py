import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="EJS Expert v6.0", layout="wide")

# 2. Style Sombre Intégral
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1A1C24; }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Expert Élastomères EJS v6.0")
st.subheader("Mode Sombre Pro - Données v5.6")

# 3. BASE DE DONNÉES (Structure v5.6 intacte)
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

# 4. Paramètres (Sidebar)
with st.sidebar:
    st.header("⚙️ Paramètres")
    f1 = st.selectbox("Sélectionner Fluide 1", fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", fluides)
    t_service = st.slider("Température (°C)", -200, 260, 20)

# 5. Calcul et Tri
df["Score"] = df[f1] + df[f2]
df_tri = df.sort_values(by="Score", ascending=False)

# 6. Affichage des Cartes EJS
st.write(f"### Résultats pour : {f1} + {f2}")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    if not temp_ok:
        color, statut = "#FF4B4B", "⚠️ HORS TEMP"
    elif row["Score"] >= 8:
        color, statut = "#00FF7F", "✅ RECOMMANDÉ"
    else:
        color, statut = "#FFA500", "⏳ VIGILANCE"

    # Bloc HTML sécurisé
    card_html = f"""
    <div style="border: 2px solid {color}; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: #1A1C24;">
        <div style="display: flex; justify-content: space-between;">
            <b style="font-size: 1.2em;">{row['Compound EJS']}</b>
            <span style="color: {color}; font-weight: bold; border: 1px solid {color}; padding: 2px 8px; border-radius: 5px;">{statut}</span>
        </div>
        <p style="margin: 10px 0 0 0;">Matière : {row['Famille']} | Score : <span style="color:{color}; font-weight:bold;">{row['Score']}/10</span></p>
        <p
