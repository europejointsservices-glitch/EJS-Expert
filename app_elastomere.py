import streamlit as st
import pandas as pd

# 1. Configuration
st.set_page_config(page_title="Expert Selecteur EJS", layout="wide")

st.title("🧪 Expert Selecteur EJS")
st.subheader("Base Intégrale : 500+ Fluides & 17 Familles d'Elastomeres")

# --- BASE DE DONNEES (Structure 17 lignes fixe) ---
data = {
    "Famille Generique": [
        "EPDM", "NBR", "Viton A", "Viton GF-S", "Viton GFLT-S", "Viton Extreme ETP", 
        "HNBR", "AFLAS (FEPM)", "FFKM (Chimie Std)", "FFKM (Alimentaire/Vapeur)", 
        "FFKM (Haute Temp)", "Silicone (VMQ)", "PTFE", 
        "Fluorosilicone (FMVQ)", "Silicone Phenyle (PMVQ)", "Caoutchouc Naturel (NR)", "Polyurethane (AU)"
    ],
    "Durete": ["70 ShA", "70 ShA", "75 ShA", "75 ShA", "75 ShA", "75 ShA", "70 ShA", "80 ShA", "75 ShA", "75 ShA", "80 ShA", "70 ShA", "60 ShD", "70 ShA", "70 ShA", "65 ShA", "90 ShA"],
    "Couleur": ["Noir", "Noir", "Noir", "Vert", "Noir", "Noir", "Noir", "Noir", "Noir", "Blanc", "Noir", "Rouge", "Blanc", "Bleu", "Gris", "Blond", "Ocre"],
    "Specificite": ["Alimentaire", "Standard", "Standard", "Chimie Severe", "Basse Temp", "Total Fluor", "Petrole", "Vapeur/Base", "Universel", "FDA/USP VI", "HT 320C", "FDA", "Total", "Hydrocarbures/Froid", "Extreme Froid", "Mecanique", "Abrasion"],
    "Temp Min": [-50, -30, -20, -15, -15, -35, -40, -10, -20, -15, -10, -60, -200, -60, -100, -50, -30],
    "Temp Max": [150, 100, 200, 230, 200, 230, 150, 200, 260, 250, 320, 200, 260, 175, 200, 80, 100],
    
    # --- OPTIONS ---
    "SANS CHOIX": [0]*17,

    # --- AGROALIMENTAIRE & NEP/SEP ---
    "Jus de Saumure 100%": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 4, 4, 3, 2],
    "Vapeur (SEP 140C)": [5, 1, 2, 3, 2, 4, 3, 5, 5, 5, 5, 3, 5, 2, 3, 1, 1],
    "Soude (NEP 2%)": [5, 4, 1, 2, 1, 4, 4, 5, 5, 5, 5, 2, 5, 2, 2, 2, 1],
    "Acide Peracetique": [5, 2, 3, 4, 4, 5, 2, 4, 5, 5, 5, 3, 5, 4, 4, 2, 2],
    "Huile de Mais": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 4, 1, 5],

    # --- CHIMIE SEVERE (Acides/Bases) ---
    "Acide Sulfurique 98%": [4, 1, 3, 5, 5, 5, 1, 3, 5, 5, 5, 1, 5, 4, 3, 1, 1],
    "Acide Chlorhydrique 37%": [5, 1, 5, 5, 5, 5, 2, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5],
    "Hypochlorite de Soude": [5, 2, 5, 5, 5, 5, 2, 4, 5, 5, 5, 3, 5, 5, 3, 2, 1],
    "Ammoniaque pur": [5, 4, 1, 1, 1, 1, 4, 5, 5, 5, 5, 4, 5, 2, 2, 5, 2],

    # --- SOLVANTS & PETROLE ---
    "Gazole / Diesel": [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 1, 1, 5],
    "Acetone / MEK": [4, 1, 1, 2, 1, 5, 1, 3, 5, 5, 5, 2, 5, 1, 2, 1, 1],
    "Benzene / Toluene": [1, 1, 5, 5, 5, 5, 1, 5, 5, 5, 5, 1, 5, 5, 1, 1, 5],
    "Skydrol LD-4": [5, 1, 1, 1, 1, 1, 1, 2, 5, 5, 5, 2, 5, 1, 5, 1, 5]
    
    # [IMPORTANT] : Vos 480 autres produits sont a inserer ici 
    # en respectant la virgule a la fin de chaque ligne.
}

# Mapping commercial
ejs_refs = {
    "AUCUNE SELECTION": None,
    "EJS-E70P": "EPDM", "EJS-N70": "NBR", "EJS-V70": "Viton A",
    "EJS-V75GF": "Viton GF-S", "EJS-V75GFLT": "Viton GFLT-S",
    "EJS-V75ETs
