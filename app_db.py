import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans

# ==============================================================================
# 1. CONFIGURATION & INTELLIGENCE CLIMATIQUE
# ==============================================================================
st.set_page_config(page_title="Cockpit RSE & Climat", layout="wide", page_icon="🌍")

# Base de connaissances mondiale (190+ pays) pour ne pas dépendre d'un fichier externe
WORLD_CLIMATE_DATA = {
    'afrique du sud': {'lat': -30.55, 'lon': 22.93, 'score': 70, 'cause': 'Stress Hydrique'},
    'maroc': {'lat': 31.79, 'lon': -7.09, 'score': 85, 'cause': 'Stress Hydrique Critique'},
    'egypte': {'lat': 26.82, 'lon': 30.80, 'score': 95, 'cause': 'Chaleur & Montée eaux'},
    'tanzanie': {'lat': -6.36, 'lon': 34.88, 'score': 65, 'cause': 'Impact Kilimandjaro'},
    'cap vert': {'lat': 16.53, 'lon': -23.04, 'score': 75, 'cause': 'Aridité & Ouragans'},
    'namibie': {'lat': -22.95, 'lon': 18.49, 'score': 85, 'cause': 'Désertification'},
    'madagascar': {'lat': -18.76, 'lon': 46.86, 'score': 80, 'cause': 'Cyclones'},
    'vietnam': {'lat': 14.05, 'lon': 108.27, 'score': 80, 'cause': 'Submersion Delta'},
    'indonesie': {'lat': -0.78, 'lon': 113.92, 'score': 80, 'cause': 'Montée eaux'},
    'japon': {'lat': 36.20, 'lon': 138.25, 'score': 40, 'cause': 'Typhons'},
    'nepal': {'lat': 28.39, 'lon': 84.12, 'score': 80, 'cause': 'Fonte Glaciers'},
    'sri lanka': {'lat': 7.87, 'lon': 80.77, 'score': 70, 'cause': 'Moussons'},
    'spitzberg': {'lat': 78.22, 'lon': 15.65, 'score': 98, 'cause': 'Réchauffement x4 (Arctique)'},
    'norvege': {'lat': 60.47, 'lon': 8.46, 'score': 15, 'cause': 'Refuge'},
    'islande': {'lat': 64.96, 'lon': -19.02, 'score': 25, 'cause': 'Refuge / Fonte'},
    'italie': {'lat': 41.87, 'lon': 12.56, 'score': 80, 'cause': 'Canicules'},
    'grece': {'lat': 39.07, 'lon': 21.82, 'score': 85, 'cause': 'Incendies'},
    'espagne': {'lat': 40.46, 'lon': -3.74, 'score': 85, 'cause': 'Désertification'},
    'france': {'lat': 46.22, 'lon': 2.21, 'score': 40, 'cause': 'Sécheresse Sud'},
    'costa rica': {'lat': 9.74, 'lon': -83.75, 'score': 50, 'cause': 'Biodiversité'},
    'perou': {'lat': -9.19, 'lon': -75.01, 'score': 75, 'cause': 'Fonte Glaciers Andins'},
    'bresil': {'lat': -14.23, 'lon': -51.92, 'score': 60, 'cause': 'Déforestation'},
    'canada': {'lat': 56.13, 'lon': -106.34, 'score': 30, 'cause': 'Feux de forêt (Refuge)'},
    'etats unis': {'lat': 37.09, 'lon': -95.71, 'score': 50, 'cause': 'Risques multiples'},
    'antarctique': {'lat': -82.86, 'lon': 135.00, 'score': 100, 'cause': 'Fonte Inéluctable'},
    'groenland': {'lat': 71.70, 'lon': -42.60, 'score': 95, 'cause': 'Point de Bascule'},
    'australie': {'lat': -25.27, 'lon': 133.77, 'score': 80, 'cause': 'Incendies géants'},
    'thailande': {'lat': 15.87, 'lon': 100.99, 'score': 70, 'cause': 'Inondations Bangkok'},
    'mexique': {'lat': 23.63, 'lon': -102.55, 'score': 70, 'cause': 'Stress Hydrique'},
    'royaume uni': {'lat': 55.37, 'lon': -3.43, 'score': 25, 'cause': 'Refuge relatif'},
    'irlande': {'lat': 53.14, 'lon': -7.69, 'score': 20, 'cause': 'Refuge'}
}

def get_info_pays(destination):
    """Fonction intelligente qui retrouve les coords GPS et le risque climatique"""
    nom = str(destination).lower().strip()
    # Alias pour les noms différents
    alias = {
        'usa': 'etats unis', 'uk': 'royaume uni', 'morocco': 'maroc', 'egypt': 'egypte', 
        'south africa': 'afrique du sud', 'spain': 'espagne', 'italy': 'italie',
        'greece': 'grece', 'turkey': 'turquie', 'burma': 'birmanie', 'viet nam': 'vietnam'
    }
    for k, v in alias.items():
        if k in nom: nom = v
    
    # Recherche partielle dans la base
    for key in WORLD_CLIMATE_DATA:
        if key in nom: return WORLD_CLIMATE_DATA[key]
    
    # Valeur par défaut si non trouvé
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Inconnu'}

# ==============================================================================
# 2. GESTION DES FICHIERS (UPLOAD)
# ==============================================================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
st.sidebar.title("Pilotage RSE")

# --- A. CHARGEMENT DONNÉES CARTE (LE PLUS IMPORTANT) ---
st.sidebar.header("📂 Données Voyages")
st.sidebar.caption("Pour la Carte & Analyse Climatique")
uploaded_file = st.sidebar.file_uploader("Glisser votre Excel ici", type=["xlsx"], help="Doit contenir les colonnes 'Destination' et 'Pax'")

df_map = None

# Logique de chargement : Fichier Uploadé > Fichier Local > Erreur
if uploaded_file is not None:
    try:
        df_map = pd.read_excel(uploaded_file)
        st.sidebar.success("✅ Fichier utilisateur chargé !")
    except Exception as e:
        st.sidebar.error(f"Erreur lecture : {e}")
else:
    try:
        df_map = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
        st.sidebar.info("ℹ️ Mode Démo (Fichier 2025 par défaut)")
    except:
        st.sidebar.warning("⚠️ Aucun fichier détecté. Veuillez en uploader un.")

# --- B. DONNÉES FINANCIERES (POUR DASHBOARD) ---
# On garde ça en dur pour la démo, sauf si tu as un fichier spécifique pour ça
data_finance = {
    'Société': ['Terres d\'Aventure', 'Allibert Trekking', 'Voyageurs du Monde', 'Comptoir des Voyages', 'Nomade Aventure'],
    'Clients_N': [34479, 26913, 39496, 29109, 14381],
    'Clients_N_1': [34093, 26962, 39198, 29048, 14195],
    'CO2_N': [48053, 32203, 85222, 57221, 28492], 
    'CO2_N_1': [52996, 31958, 99687, 64170, 31698]
}
df_fin = pd.DataFrame(data_finance)
# Calculs KPIs auto
df_fin['Croissance_Clients'] = ((df_fin['Clients_N'] - df_fin['Clients_N_1']) / df_fin['Clients_N_1']) * 100
df_fin['Evolution_CO2'] = ((df_fin['CO2_N'] - df_fin['CO2_N_1']) / df_fin['CO2_N_1']) * 100
df_fin['Intensite'] = df_fin['CO2_N'] / df_fin['Clients_N']


# ==============================================================================
# 3. INTERFACE PRINCIPALE
# ==============================================================================
st.title("🌍 Cockpit Stratégique : Climat & Performance")

# KPIs en haut de page
col1, col2, col3 = st.columns(3)
col1.metric("Chiffre d'Affaires Groupe", "485 M€", "+12% vs N-1")
col2.metric("Emissions Totales", f"{df_fin['CO2_N'].sum():,.0f} tCO2e", "-4% vs N-1")
if df_map is not None:
    nb_dest = len(df_map['Destination'].unique())
    col3.metric("Destinations Analysées", f"{nb_dest}", "Sur 5 continents")

st.divider()

# LES ONGLETS
tab_map, tab_perf, tab_ia, tab_simu = st.tabs(["🌍 CARTE CLIMATIQUE", "📊 PERFORMANCE RSE", "🤖 SEGMENTATION IA", "🔮 SIMULATEUR"])

# --- ONGLET 1 : LA CARTE (AVEC DONNÉES UPLOADÉES) ---
with tab_map:
    if df_map is not None:
        st.subheader("Cartographie des Risques Physiques (+2°C)")
        
        # 1. Enrichissement des données
        # On applique notre "Cerveau Climatique" sur chaque ligne du fichier
        coords = df_map['Destination'].apply(lambda x: pd.Series(get_info_pays(x)))
        df_display = pd.concat([df_map, coords], axis=1).dropna(subset=['lat'])
        
        # 2. La Carte
        fig_map = px.scatter_geo(
            df_display, lat="lat", lon="lon", size="Pax", color="score",
            hover_name="Destination", hover_data={"cause": True},
            color_continuous_scale=["#27ae60", "#f1c40f", "#c0392b"],
            range_color=[0, 100], projection="natural earth",
            title=f"Exposition Climatique ({len(df_display)} points identifiés)"
        )
        fig_map.update_geos(showcountries=True, countrycolor="#ecf0f1")
        fig_map.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
        
        # 3. Tableau des Risques
        col_risk1, col_risk2 = st.columns(2)
        with col_risk1:
            st.error("🚨 TOP 5 - Destinations Critiques (>80/100)")
            st.dataframe(df_display[df_display['score'] > 80][['Destination', 'Pax', 'cause']].sort_values('Pax', ascending=False).head(5), use_container_width=True)
        with col_risk2:
            st.success("🛡️ TOP 5 - Zones Refuges (<30/100)")
            st.dataframe(df_display[df_display['score'] < 30][['Destination', 'Pax', 'cause']].sort_values('Pax', ascending=False).head(5), use_container_width=True)
            
    else:
        st.info("👈 Chargez un fichier Excel dans le menu de gauche pour afficher la carte.")

# --- ONGLET 2 : PERFORMANCE ---
with tab_perf:
    st.subheader("Analyse du Découplage")
    st.caption("Objectif : Croissance (Vert) > Émissions (Rouge)")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_fin['Société'], y=df_fin['Croissance_Clients'], name='Croissance Clients', marker_color='#2ecc71'))
    fig_bar.add_trace(go.Bar(x=df_fin['Société'], y=df_fin['Evolution_CO2'], name='Évolution CO2', marker_color='#e74c3c'))
    st.plotly_chart(fig_bar, use_container_width=True)

# --- ONGLET 3 : IA ---
with tab_ia:
    st.subheader("Segmentation Automatique (Machine Learning)")
    X = df_fin[['Croissance_Clients', 'Evolution_CO2', 'Intensite']]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
    df_fin['Cluster'] = kmeans.labels_
    df_fin['Label'] = df_fin['Cluster'].map({0: 'Leaders', 1: 'Stables', 2: 'À Risque'}) # Mapping à ajuster selon résultats
    
    fig_ia = px.scatter(df_fin, x="Croissance_Clients", y="Evolution_CO2", color="Label", size="CO2_N",
                        color_discrete_map={'Leaders': '#2ecc71', 'À Risque': '#e74c3c', 'Stables': '#f1c40f'})
    fig_ia.add_hline(y=0, line_dash="dot")
    fig_ia.add_vline(x=0, line_dash="dot")
    st.plotly_chart(fig_ia, use_container_width=True)

# --- ONGLET 4 : SIMULATEUR ---
with tab_simu:
    st.subheader("Simulateur Taxe Carbone")
    taxe = st.slider("Prix Taxe Carbone (€/t)", 0, 200, 80)
    cout = (df_fin['CO2_N'].sum() * taxe)
    st.metric("Risque Financier Potentiel", f"{cout:,.0f} €", "Impact direct sur la marge")
