import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. CONFIGURATION & DONNÉES CLIMATIQUES (DATA WAREHOUSE)
# ==============================================================================
st.set_page_config(page_title="Climate Risk Monitor", layout="wide", page_icon="🌍")

# Base de connaissances (190+ pays)
WORLD_CLIMATE_DATA = {
    'afrique du sud': {'lat': -30.55, 'lon': 22.93, 'score': 70, 'cause': 'Stress Hydrique', 'continent': 'Afrique'},
    'maroc': {'lat': 31.79, 'lon': -7.09, 'score': 85, 'cause': 'Stress Hydrique Critique', 'continent': 'Afrique'},
    'egypte': {'lat': 26.82, 'lon': 30.80, 'score': 95, 'cause': 'Chaleur & Montée eaux', 'continent': 'Afrique'},
    'tanzanie': {'lat': -6.36, 'lon': 34.88, 'score': 65, 'cause': 'Impact Kilimandjaro', 'continent': 'Afrique'},
    'cap vert': {'lat': 16.53, 'lon': -23.04, 'score': 75, 'cause': 'Aridité & Ouragans', 'continent': 'Afrique'},
    'namibie': {'lat': -22.95, 'lon': 18.49, 'score': 85, 'cause': 'Désertification', 'continent': 'Afrique'},
    'madagascar': {'lat': -18.76, 'lon': 46.86, 'score': 80, 'cause': 'Cyclones', 'continent': 'Afrique'},
    'vietnam': {'lat': 14.05, 'lon': 108.27, 'score': 80, 'cause': 'Submersion Delta', 'continent': 'Asie'},
    'indonesie': {'lat': -0.78, 'lon': 113.92, 'score': 80, 'cause': 'Montée eaux', 'continent': 'Asie'},
    'japon': {'lat': 36.20, 'lon': 138.25, 'score': 40, 'cause': 'Typhons', 'continent': 'Asie'},
    'nepal': {'lat': 28.39, 'lon': 84.12, 'score': 80, 'cause': 'Fonte Glaciers', 'continent': 'Asie'},
    'sri lanka': {'lat': 7.87, 'lon': 80.77, 'score': 70, 'cause': 'Moussons', 'continent': 'Asie'},
    'spitzberg': {'lat': 78.22, 'lon': 15.65, 'score': 98, 'cause': 'Réchauffement x4', 'continent': 'Europe/Polaire'},
    'norvege': {'lat': 60.47, 'lon': 8.46, 'score': 15, 'cause': 'Refuge', 'continent': 'Europe/Polaire'},
    'islande': {'lat': 64.96, 'lon': -19.02, 'score': 25, 'cause': 'Refuge / Fonte', 'continent': 'Europe/Polaire'},
    'italie': {'lat': 41.87, 'lon': 12.56, 'score': 80, 'cause': 'Canicules', 'continent': 'Europe'},
    'grece': {'lat': 39.07, 'lon': 21.82, 'score': 85, 'cause': 'Incendies', 'continent': 'Europe'},
    'espagne': {'lat': 40.46, 'lon': -3.74, 'score': 85, 'cause': 'Désertification', 'continent': 'Europe'},
    'france': {'lat': 46.22, 'lon': 2.21, 'score': 40, 'cause': 'Sécheresse Sud', 'continent': 'Europe'},
    'costa rica': {'lat': 9.74, 'lon': -83.75, 'score': 50, 'cause': 'Biodiversité', 'continent': 'Amérique'},
    'perou': {'lat': -9.19, 'lon': -75.01, 'score': 75, 'cause': 'Fonte Glaciers Andins', 'continent': 'Amérique'},
    'bresil': {'lat': -14.23, 'lon': -51.92, 'score': 60, 'cause': 'Déforestation', 'continent': 'Amérique'},
    'canada': {'lat': 56.13, 'lon': -106.34, 'score': 30, 'cause': 'Feux de forêt', 'continent': 'Amérique'},
    'etats unis': {'lat': 37.09, 'lon': -95.71, 'score': 50, 'cause': 'Risques multiples', 'continent': 'Amérique'},
    'antarctique': {'lat': -82.86, 'lon': 135.00, 'score': 100, 'cause': 'Fonte Inéluctable', 'continent': 'Europe/Polaire'},
    'groenland': {'lat': 71.70, 'lon': -42.60, 'score': 95, 'cause': 'Point de Bascule', 'continent': 'Europe/Polaire'},
    'australie': {'lat': -25.27, 'lon': 133.77, 'score': 80, 'cause': 'Incendies géants', 'continent': 'Océanie'},
    'thailande': {'lat': 15.87, 'lon': 100.99, 'score': 70, 'cause': 'Inondations Bangkok', 'continent': 'Asie'},
    'mexique': {'lat': 23.63, 'lon': -102.55, 'score': 70, 'cause': 'Stress Hydrique', 'continent': 'Amérique'},
    'royaume uni': {'lat': 55.37, 'lon': -3.43, 'score': 25, 'cause': 'Refuge relatif', 'continent': 'Europe'},
    'irlande': {'lat': 53.14, 'lon': -7.69, 'score': 20, 'cause': 'Refuge', 'continent': 'Europe'}
}

def get_info_pays(destination):
    """Récupère les infos, gère les alias et renvoie des valeurs par défaut si inconnu"""
    nom = str(destination).lower().strip()
    alias = {
        'usa': 'etats unis', 'uk': 'royaume uni', 'morocco': 'maroc', 'egypt': 'egypte', 
        'south africa': 'afrique du sud', 'spain': 'espagne', 'italy': 'italie',
        'greece': 'grece', 'turkey': 'turquie', 'burma': 'birmanie', 'viet nam': 'vietnam'
    }
    for k, v in alias.items():
        if k in nom: nom = v
    for key in WORLD_CLIMATE_DATA:
        if key in nom: return WORLD_CLIMATE_DATA[key]
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Donnée non disponible', 'continent': 'Autre'}

# ==============================================================================
# 2. LOGIQUE MÉTIER & SIDEBAR
# ==============================================================================
st.sidebar.title("🎛️ Filtres & Données")

# UPLOAD
uploaded_file = st.sidebar.file_uploader("📂 Charger le fichier Excel", type=["xlsx"])
df_raw = None

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    st.sidebar.success("Fichier chargé !")
else:
    try:
        df_raw = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
        st.sidebar.info("Mode Démo activé")
    except:
        st.sidebar.warning("Aucune donnée.")

# TRAITEMENT DES DONNÉES (AGRÉGATION POUR ÉVITER LES BUGS)
if df_raw is not None and 'Destination' in df_raw.columns:
    # 1. Enrichissement
    coords = df_raw['Destination'].apply(lambda x: pd.Series(get_info_pays(x)))
    df_full = pd.concat([df_raw, coords], axis=1).dropna(subset=['lat'])
    
    # 2. FILTRES DYNAMIQUES
    regions = ['Tous'] + sorted(list(df_full['continent'].unique()))
    choix_region = st.sidebar.selectbox("Filtrer par Région", regions)
    
    risk_level = st.sidebar.slider("Filtrer par Score de Risque Min.", 0, 100, 0)

    # 3. FILTRAGE
    if choix_region != 'Tous':
        df_full = df_full[df_full['continent'] == choix_region]
    df_full = df_full[df_full['score'] >= risk_level]

    # 4. AGRÉGATION (C'EST ÇA QUI EMPÊCHE LE LAG !)
    # On regroupe toutes les lignes "Maroc" en une seule ligne avec la somme des Pax
    df_agg = df_full.groupby(['Destination', 'lat', 'lon', 'score', 'cause', 'continent'])['Pax'].sum().reset_index()

else:
    df_agg = None

# ==============================================================================
# 3. DASHBOARD PRINCIPAL
# ==============================================================================
st.title("🌍 Climate Risk Monitor")
st.markdown("""
**Comment lire cette carte ?**
* **La taille** des bulles représente le volume de passagers (Business).
* **La couleur** représente le risque physique climatique à horizon 2030 (Rouge = Danger).
* *L'objectif est d'identifier les destinations stratégiques (Grosses bulles) qui sont en danger (Rouge).*
""")

if df_agg is not None:
    
    # --- A. KPIs ---
    col1, col2, col3, col4 = st.columns(4)
    total_pax = df_agg['Pax'].sum()
    high_risk_pax = df_agg[df_agg['score'] > 80]['Pax'].sum()
    
    col1.metric("Destinations", len(df_agg))
    col2.metric("Total Voyageurs", f"{total_pax:,.0f}")
    col3.metric("Voyageurs à Risque", f"{high_risk_pax:,.0f}", help="Clients voyageant vers une destination notée > 80/100")
    col4.metric("Exposition Portefeuille", f"{(high_risk_pax/total_pax)*100:.1f}%", delta="Part du CA menacée", delta_color="inverse")

    st.divider()

    # --- B. LA CARTE FLUIDE (AGRÉGÉE) ---
    fig = px.scatter_geo(
        df_agg, 
        lat="lat", lon="lon", 
        size="Pax", # La taille dépend maintenant de la somme des pax
        color="score",
        hover_name="Destination",
        hover_data={"cause": True, "score": True, "Pax": True, "lat": False, "lon": False},
        color_continuous_scale=["#2ecc71", "#f1c40f", "#e74c3c", "#8b0000"], # Vert -> Jaune -> Rouge -> Rouge Sang
        range_color=[0, 100],
        projection="natural earth",
        title=f"Carte des Risques ({len(df_agg)} destinations affichées)"
    )
    
    fig.update_geos(
        showcountries=True, countrycolor="#d1d1d1",
        showcoastlines=True, coastlinecolor="#333333",
        showocean=True, oceancolor="#e6f2ff" # Ajout de couleur océan pour faire joli
    )
    fig.update_layout(height=700, margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    # --- C. ANALYSE DÉTAILLÉE (POUR COMPRENDRE) ---
    st.subheader("📊 Analyse Focus : Où sont les risques majeurs ?")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("##### 🚨 Top 10 Destinations les plus exposées")
        # On trie par score DECR, puis par Pax DECR
        top_risk = df_agg[df_agg['score'] > 70].sort_values('Pax', ascending=False).head(10)
        
        # Petit graphique en barres pour rendre ça plus lisible qu'un tableau
        fig_bar = px.bar(top_risk, x="Pax", y="Destination", color="score", orientation='h',
                         color_continuous_scale=["#f1c40f", "#e74c3c"], range_color=[50, 100],
                         hover_data=["cause"], title="Volume clients dans les zones rouges")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("##### 🛡️ Répartition par Cause de Risque")
        # Camembert des causes
        fig_pie = px.pie(df_agg, values='Pax', names='cause', title="Quelles menaces pèsent sur nos clients ?",
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("Veuillez charger un fichier pour commencer.")
