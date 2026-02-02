import streamlit as st
import pandas as pd

# 1. Configuration (Retour au mode large v5.6)
st.set_page_config(page_title="EJS Expert v6.6", layout="wide")

st.title("🧪 Expert Élastomères EJS v6.6")
st.subheader("Filtre DRC Dynamique & Performance")

# --- BASE DE DONNÉES (Strictement inchangée) ---
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

# --- LOGIQUE DE TRADUCTION DRC (Sans changer la base) ---
def evaluer_drc(row):
    if any(x in row["Famille"] for x in ["PTFE", "FKM"]):
        return "Excellente"
    elif any(x in row["Famille"] for x in ["EPDM", "NBR"]):
        return "Moyenne"
    else:
        return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR (PARAMÈTRES CORRIGÉS) ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    # Liste des fluides filtrée pour exclure les colonnes techniques
    cols_tech = ["Compound EJS", "Famille", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = [c for c in df.columns if c not in cols_tech]
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    st.write("---")
    # Filtre qualitatif DRC demandé
    choix_drc = st.multiselect(
        "Filtrer par Qualité DRC", 
        ["Excellente", "Moyenne", "Basse"], 
        default=["Excellente", "Moyenne", "Basse"]
    )

# --- FILTRAGE ET CALCUL ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- AFFICHAGE ---
st.write(f"### 📊 Synthèse Comparative : {f1} + {f2}")
st.dataframe(df_tri.drop(columns=["Qualité DRC"]), use_container_width=True)

st.write("---")
st.write("### 📑 Fiches d'Expertise Détaillées")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    color = "#28a745" if row["Score"] >= 8 and temp_ok else "#fd7e14"
    if not temp_ok: color = "#dc3545"

    st.markdown(f"""
        <div style="border: 3px solid {color}; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: white;">
            <b style="font-size: 1.1em; color: black;">{row['Compound EJS']} ({row['Famille']})</b><br>
            <span style="color:{color}; font-weight:bold;">Note : {row['Score']}/10 | DRC : {row['Qualité DRC']}</span><br>
            <small style="color: black;">Dureté : {row['Dureté']} | Temp : {row['Temp Min']}°C / {row['Temp Max']}°C</small>
        </div>
    """, unsafe_allow_html=True)
