import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="EJS - Expert Elastomères v5.6", layout="wide")

# --- STYLE VISUEL ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117 !important; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    .card {
        background-color: #1a1c24 !important;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #30363d;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .ref-badge {
        background-color: #f39c12; color: black; padding: 2px 8px;
        border-radius: 4px; font-weight: bold; font-size: 0.85em;
    }
    .synopsis-table { width: 100%; border-collapse: collapse; color: white; font-size: 0.85em; margin-bottom: 20px;}
    .synopsis-table td, .synopsis-table th { border: 1px solid #30363d; padding: 8px; }
    [data-testid="stSidebar"] { background-color: #262730 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENTETE ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔬 Expert Élastomères - EJS")
    st.write("### Europe Joints Services | Classement par Performance Technique")
with col2:
    st.markdown('<div style="background-color:#f39c12; color:white; padding:15px; border-radius:8px; text-align:center; font-weight:bold; margin-top:10px;">EUROPE JOINTS SERVICES</div>', unsafe_allow_html=True)

# --- BASE DE DONNÉES MASSIVE (45 FLUIDES) ---
data = {
    "Code ISO/ASTM": ["NBR", "EPDM (S)", "EPDM (P)", "FKM (Std)", "FKM (GF)", "FKM (GLT)", "FKM (GBLT)", "FKM (ETP)", "HNBR", "TFEPM", "FFKM", "VMQ", "PVMQ"],
    "Ref_EJS": ["EJS-N70", "EJS-E70S", "EJS-E70P", "EJS-V70A", "EJS-V70GF", "EJS-V70LT", "EJS-V70GB", "EJS-V70ETP", "EJS-H70", "EJS-AFL75", "EJS-FF75", "EJS-S70", "EJS-S70LT"],
    "Désignation": ["Nitrile", "EPDM Soufre", "EPDM Peroxyde", "Viton A", "Viton GF", "Viton GLT", "Viton GBLT", "Viton Extreme", "Nitrile Hydr.", "Aflas", "Perfluoro", "Silicone Std", "Silicone Phénylé"],
    "Temp_Min": [-30, -45, -50, -20, -15, -40, -40, -15, -40, -5, -15, -60, -100],
    "Temp_Max": [100, 120, 150, 200, 210, 200, 210, 210, 150, 200, 320, 230, 200],
    "DRC": [4, 3, 5, 5, 4, 4, 4, 3, 4, 2, 5, 5, 4],
    
    # HYDROCARBURES & CARBURANTS
    "Gazole / Diesel": [5, 1, 1, 5, 5, 5, 5, 5, 5, 4, 5, 1, 1],
    "Essence (Bio E10)": [3, 1, 1, 3, 5, 3, 5, 5, 4, 2, 5, 1, 1],
    "Kérosène (Jet A1)": [5, 1, 1, 5, 5, 5, 5, 5, 5, 3, 5, 1, 1],
    "Fuel Lourd": [5, 1, 1, 5, 5, 5, 5, 5, 5, 4, 5, 2, 2],
    "Huile Minérale": [5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4],
    "Huile Silicone": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1],
    "Graisse Lithium": [5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4],
    
    # ACIDES
    "Acide Sulfurique 98%": [1, 2, 2, 4, 5, 3, 5, 5, 1, 5, 5, 1, 1],
    "Acide Chlorhydrique 37%": [1, 3, 3, 5, 5, 5, 5, 5, 1, 5, 5, 1, 1],
    "Acide Nitrique": [1, 1, 1, 3, 4, 2, 4, 5, 1, 4, 5, 1, 1],
    "Acide Phosphorique": [2, 4, 4, 5, 5, 5, 5, 5, 2, 5, 5, 2, 2],
    "Acide Acétique": [2, 5, 5, 1, 1, 1, 1, 2, 2, 5, 5, 4, 4],
    "Acide Formique": [2, 4, 4, 2, 2, 2, 2, 3, 2, 4, 5, 3, 3],
    
    # BASES & AGRO (NEP/SEP)
    "Soude Caustique 50%": [4, 5, 5, 1, 1, 1, 1, 4, 4, 5, 5, 2, 2],
    "Potasse (KOH)": [4, 5, 5, 1, 1, 1, 1, 4, 4, 5, 5, 2, 2],
    "Ammoniaque": [4, 5, 5, 1, 1, 1, 1, 2, 4, 5, 5, 4, 4],
    "NEP Acide (CIP)": [1, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 3, 3],
    "NEP Basique (CIP)": [2, 5, 5, 1, 1, 1, 1, 4, 3, 5, 5, 2, 2],
    "SEP Vapeur (SIP)": [1, 4, 5, 1, 2, 1, 2, 3, 2, 5, 5, 3, 3],
    "Eau Oxygénée": [2, 5, 5, 4, 5, 4, 5, 5, 3, 5, 5, 4, 4],
    "Hypochlorite (Javel)": [2, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 3, 3],
    
    # SOLVANTS & ALCOOLS
    "Acétone": [1, 5, 5, 1, 1, 1, 1, 1, 1, 4, 5, 2, 2],
    "Méthanol": [3, 4, 4, 2, 4, 1, 4, 4, 3, 4, 5, 5, 5],
    "Éthanol": [4, 5, 5, 4, 5, 4, 5, 5, 4, 5, 5, 5, 5],
    "Isopropanol": [4, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5],
    "Toluène / Benzène": [1, 1, 1, 5, 5, 5, 5, 5, 1, 1, 5, 1, 1],
    "Xylène": [1, 1, 1, 5, 5, 5, 5, 5, 1, 1, 5, 1, 1],
    "MEK / MIBK": [1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1],
    "Éthyl Acétate": [1, 4, 4, 1, 1, 1, 1, 1, 1, 2, 5, 2, 2],
    "Trichloroéthylène": [1, 1, 1, 5, 5, 5, 5, 5, 1, 1, 5, 1, 1],
    "Chlorure de Méthylène": [1, 1, 1, 4, 4, 4, 4, 4, 1, 1, 5, 1, 1],
    
    # FLUIDES TECHNIQUES & GAZ
    "Eau_Vapeur (>150°C)": [1, 3, 5, 1, 3, 1, 3, 4, 2, 5, 5, 3, 3],
    "Skydrol LD4": [1, 5, 5, 1, 1, 1, 1, 1, 1, 4, 5, 1, 1],
    "Liquide de Frein (DOT4)": [1, 5, 5, 1, 1, 1, 1, 1, 1, 4, 5, 2, 2],
    "Liquide de Refroidissement": [4, 5, 5, 3, 4, 3, 4, 4, 4, 5, 5, 4, 4],
    "Fréon R134a": [4, 2, 2, 3, 3, 3, 3, 3, 5, 1, 5, 1, 1],
    "Ozone / UV": [2, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5],
    "H2S (Gaz Acide)": [2, 3, 3, 3, 4, 3, 4, 5, 4, 5, 5, 1, 1],
    "Chlore (Sec)": [1, 2, 2, 5, 5, 5, 5, 5, 1, 4, 5, 1, 1],
    "Oxygène": [2, 4, 4, 5, 5, 5, 5, 5, 3, 4, 5, 5, 5],
    "Hydrogène": [4, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5],
    "Azote": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Vide Poussé": [3, 1, 1, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5],
    
    "Indice_Prix": [1.0, 1.2, 1.6, 4.0, 6.5, 8.0, 12.0, 18.0, 4.0, 8.0, 100.0, 3.0, 9.0]
}
df = pd.DataFrame(data)

# --- FILTRES ---
with st.sidebar:
    st.header("⚙️ Configuration")
    t_req = st.slider("Température de service (°C)", -100, 320, 20)
    fluides_dispos = [c for c in df.columns if c not in ["Code ISO/ASTM", "Ref_EJS", "Désignation", "Temp_Min", "Temp_Max", "Indice_Prix", "DRC"]]
    f1 = st.selectbox("Fluide Principal", sorted(fluides_dispos), index=19) # NEP Basique
    f2 = st.selectbox("Fluide Secondaire", sorted(fluides_dispos), index=26) # SEP Vapeur
    drc_critique = st.checkbox("Exigence DRC Critique")
    search_ref = st.text_input("🔍 Rechercher une référence EJS")

# --- CALCUL DU SCORE DE PERFORMANCE ---
df['Score_Tech'] = df[f1] + df[f2]

# --- LOGIQUE DE FILTRAGE & CLASSEMENT ---
mask = (df['Temp_Max'] >= t_req) & (df['Temp_Min'] <= t_req) & (df[f1] > 1) & (df[f2] > 1)
if drc_critique: mask &= (df['DRC'] >= 4)
if search_ref: mask &= (df['Ref_EJS'].str.contains(search_ref, case=False))

# CLASSEMENT : Performance (Décroissant) puis Prix (Croissant)
valides = df[mask].sort_values(by=["Score_Tech", "Indice_Prix"], ascending=[False, True])

# --- SYNOPSIS ---
with st.expander("📖 Synopsis des graduations (1 à 5)", expanded=True):
    st.markdown("""
    <table class="synopsis-table">
        <tr><th>Note</th><th>Signification</th><th>Effet / Usage EJS</th></tr>
        <tr><td><b>5</b></td><td>Excellente</td><td>Gonflement &lt; 10%. Idéal.</td></tr>
        <tr><td><b>4</b></td><td>Bonne</td><td>Gonflement 10-20%. Validé standard.</td></tr>
        <tr><td><b>3</b></td><td>Moyenne</td><td>Gonflement 20-40%. <b>Usage statique uniquement</b>.</td></tr>
        <tr><td><b>2</b></td><td>Faible</td><td>Gonflement &gt; 40%. Déconseillé.</td></tr>
        <tr><td><b>1</b></td><td>Nulle</td><td><b>INTERDIT</b>. Destruction du joint.</td></tr>
    </table>
    """, unsafe_allow_html=True)

# --- AFFICHAGE ---
st.divider()
if not valides.empty:
    st.subheader(f"✅ Classement des matériaux compatibles ({f1} + {f2})")
    cols = st.columns(3)
    for i, (_, row) in enumerate(valides.iterrows()):
        with cols[i % 3]:
            border_color = "#27ae60" if (row[f1] >= 4 and row[f2] >= 4) else "#f39c12"
            st.markdown(f"""
                <div class="card" style="border-left: 12px solid {border_color};">
                    <span class="ref-badge">{row['Ref_EJS']}</span>
                    <h3 style="margin:5px 0 0 0; color:{border_color} !important;">{row['Code ISO/ASTM']}</h3>
                    <p style="font-size:0.85em; margin-bottom:10px;"><i>{row['Désignation']}</i></p>
                    <p style="margin:0; font-size:0.9em;">🧪 {f1}: <b>{row[f1]}/5</b> | {f2}: <b>{row[f2]}/5</b></p>
                    <p style="margin:0; font-size:0.9em;">🔄 DRC: <b>{row['DRC']}/5</b> | 🌡️ {row['Temp_Min']}/{row['Temp_Max']}°C</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("❌ Aucune solution trouvée pour ce mélange complexe à cette température.")

# --- TABLEAU FINAL ---
st.divider()
st.subheader("📊 Tableau comparatif (trié par performance)")
st.dataframe(valides.drop(columns=['Score_Tech']), use_container_width=True, hide_index=True)
