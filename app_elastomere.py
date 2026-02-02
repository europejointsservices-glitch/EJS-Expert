import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="EJS Expert v9.6", layout="wide")

st.title("🧪 Expert Élastomères EJS v9.6")
st.subheader("Base 100 Fluides - Spécialités & Jus de Saumure 100%")

# --- BASE DE DONNÉES ENRICHIE ---
data = {
    "Famille Générique": [
        "EPDM", "NBR", "Viton™ A (Standard)", "Viton™ GBL-S", 
        "Viton™ GF-S", "Viton™ GFLT-S", "Viton™ Extreme ETP", 
        "AFLAS (FEPM)", "HNBR", "Silicone", "PTFE"
    ],
    "Dureté": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "80 ShA", "70 ShA", "70 ShA", "60 ShD"],
    "Couleur": ["Noir", "Noir", "Noir", "Noir", "Vert", "Noir", "Noir", "Noir", "Noir", "Rouge", "Blanc"],
    "Spécificité": ["Alimentaire", "Standard", "Standard", "Haute teneur Fluor", "Chimie Sévère", "Basse Température", "Universalité Chimique", "Vapeur/Base", "Pétrole/Chaleur", "FDA", "Total"],
    "Temp Min": [-50, -30, -20, -15, -15, -35, -10, -10, -40, -60, -200],
    "Temp Max": [150, 100, 200, 210, 230, 200, 230, 200, 150, 200, 260],
    
    # --- FLUIDES AGROALIMENTAIRES ---
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5],
    "Vapeur (SEP 140°C)": [5, 1, 2, 2, 3, 2, 4, 5, 3, 3, 5],
    "Soude (NEP 2%)": [5, 4, 1, 1, 2, 1, 4, 5, 4, 2, 5],
    "Lait / Produits Laitiers": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Jus de Fruits": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    
    # --- CHIMIE & INDUSTRIE ---
    "Acide Chlorhydrique 37%": [5, 1, 5, 5, 5, 5,
