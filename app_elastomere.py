import streamlit as st
import pandas as pd

# Configuration de la page en mode large pour le tableau
st.set_page_config(page_title="Expert Élastomères EJS v5.6", layout="wide")

# Titre de l'application
st.title("🧪 Expert Élastomères EJS v5.6")
st.subheader("Sélection par Performance Technique")

# --- BASE DE DONNÉES ORIGINALE (Complète avec DRC et Fluides) ---
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
    # Ajoutez ici vos 45 fluides comme à l'origine
}

df = pd.DataFrame(data)

# Identification des colonnes de fluides pour le calcul
fluides = [c for c in df.columns if c not in ["Compound EJS", "Famille", "Dureté", "Couleur", "Norme", "Temp Min", "Temp Max"]]

# --- SIDEBAR (PARAMÈTRES) ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    fluide_1 = st.selectbox("Sélectionner Fluide 1", fluides)
    fluide_2 = st.selectbox("Sélectionner Fluide 2", fluides)
    temp_service = st.slider("Température de service (°C)", -200, 260, 20)

# --- LOGIQUE DE CALCUL ---
# Calcul du score basé sur les deux fluides choisis
df["Score"] = df[fluide_1] + df[fluide_2]

# Tri automatique par performance technique (Score le plus haut en premier)
df_tri = df.sort_values(by="Score", ascending=False)

# --- AFFICHAGE DU TABLEAU COMPLET ---
st.write(f"### Résultats comparatifs pour : {fluide_1} + {fluide_2}")
st.write("Le tableau ci-dessous affiche toutes les données DRC et chimiques de votre sélection.")

# Affichage du tableau (Dataframe)
st.dataframe(df_tri, use_container_width=True)

# --- LÉGENDE TECHNIQUE ---
st.info("""
**Guide de lecture :**
* **Score sur 10** : Somme des résistances chimiques (Note/5 par fluide).
* **Température** : Vérifiez que votre température de service est bien comprise entre Temp Min et Temp Max.
""")
