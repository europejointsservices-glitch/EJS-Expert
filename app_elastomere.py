import streamlit as st
import pandas as pd

# 1. Configuration (Mode large v5.6)
st.set_page_config(page_title="EJS Expert v7.0", layout="wide")

st.title("🧪 Expert Élastomères EJS v7.0")
st.subheader("Analyse Technique & Expertise Visuelle")

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

# --- LOGIQUE DRC (Filtre qualitatif automatique) ---
def evaluer_drc(row):
    if any(x in row["Famille"] for x in ["PTFE", "FKM"]): return "Excellente"
    elif any(x in row["Famille"] for x in ["EPDM", "NBR"]): return "Moyenne"
    else: return "Basse"

df["Qualité DRC"] = df.apply(evaluer_drc, axis=1)

# --- SIDEBAR : PARAMÈTRES D'EXPERTISE ---
with st.sidebar:
    st.header("⚙️ Configuration")
    cols_tech = ["Compound EJS", "Famille", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max", "Qualité DRC"]
    liste_fluides = [c for c in df.columns if c not in cols_tech]
    
    f1 = st.selectbox("Sélectionner Fluide 1", liste_fluides)
    f2 = st.selectbox("Sélectionner Fluide 2", liste_fluides)
    t_service = st.slider("Température de service (°C)", -200, 260, 20)
    
    st.write("---")
    choix_drc = st.multiselect("Filtrer par Qualité DRC", ["Excellente", "Moyenne", "Basse"], default=["Excellente", "Moyenne", "Basse"])

# --- CALCULS ET TRI ---
df["Score"] = df[f1] + df[f2]
df_tri = df[df["Qualité DRC"].isin(choix_drc)].sort_values(by="Score", ascending=False)

# --- SYNOPSIS ---
st.info(f"🧐 **Synopsis :** Étude sur **{f1}** et **{f2}**. Les couleurs de fond indiquent le niveau de recommandation.")

# --- SECTION 1 : FICHES DÉTAILLÉES AVEC FONDS TRANSPARENTS ---
st.write("### 📑 Détail des Notes et Synopsis par Matériau")

for index, row in df_tri.iterrows():
    temp_ok = row["Temp Min"] <= t_service <= row["Temp Max"]
    
    # Définition des couleurs RGBA (20% de transparence = 0.2)
    if not temp_ok:
        border_color = "#dc3545" # Rouge
        bg_color = "rgba(220, 53, 69, 0.2)"
    elif row["Score"] >= 8:
        border_color = "#28a745" # Vert
        bg_color = "rgba(40, 167, 69, 0.2)"
    else:
        border_color = "#fd7e14" # Orange
        bg_color = "rgba(253, 126, 20, 0.2)"

    st.markdown(f"""
        <div style="border: 3px solid {border_color}; border-radius: 12px; padding: 20px; margin-bottom: 15px; background-color: {bg_color}; color: black;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 1.3em;">{row['Compound EJS']} ({row['Famille']})</b>
                <b style="font-size: 1.2em; color: black; background: white; padding: 2px 8px; border-radius: 5px;">Score : {row['Score']}/10</b>
            </div>
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid {border_color}; opacity: 0.3;">
            <p style="margin: 5px 0;"><b>🔍 Synopsis des notes chimiques :</b></p>
            <ul style="margin: 5px 0; font-size: 0.95em;">
                <li>{f1} : <b>{row[f1]}/5</b></li>
                <li>{f2} : <b>{row[f2]}/5</b></li>
            </ul>
            <p style="margin: 10px 0 0 0; font-size: 0.9em; line-height: 1.4;">
            <b>Qualité DRC :</b> {row['Qualité DRC']} | <b>Dureté :</b> {row['Dureté']} | <b>Couleur :</b> {row['Couleur']}<br>
            <b>Plage :</b> {row['Temp Min']}°C à {row['Temp Max']}°C
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- SECTION 2 : TABLEAU RÉCAPITULATIF ---
st.write("---")
st.write("### 📊 Synthèse Comparative Complète")
st.dataframe(df_tri.drop(columns=["Qualité DRC"]), use_container_width=True)
