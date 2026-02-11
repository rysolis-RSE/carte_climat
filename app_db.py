import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. CONFIGURATION & INTELLIGENCE CLIMATIQUE MONDIALE
# ==============================================================================
st.set_page_config(page_title="Risk Map Climatique", layout="wide", page_icon="🌍")

# Base de connaissances mondiale (Coords + Risques GIEC)
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
    'spitzberg': {'lat': 78.22, 'lon': 15.65, 'score': 98, 'cause': 'Réchauffement x4 (Arctique)'},
    'norvege': {'lat': 60.47, 'lon': 8.46, 'score': 15, 'cause': 'Zone Refuge'},
    'islande': {'lat': 64.96, 'lon': -19.02, 'score': 25, 'cause': 'Refuge / Fonte'},
    'italie': {'lat': 41.87, 'lon': 12.56, 'score': 80, 'cause': 'Canicules'},
    'grece': {'lat': 39.07, 'lon': 21.82, 'score': 85, 'cause': 'Incendies'},
    'espagne': {'lat': 40.46, 'lon': -3.74, 'score': 85, 'cause': 'Désertification'},
    'france': {'lat': 46.22, 'lon': 2.21, 'score': 40, 'cause': 'Sécheresse Sud'},
    'costa rica': {'lat': 9.74, 'lon': -83.75, 'score': 50, 'cause': 'Biodiversité'},
    'perou': {'lat': -9.19, 'lon': -75.01, 'score': 75, 'cause': 'Fonte Glaciers Andins'},
    'canada': {'lat': 56.13, 'lon': -106.34, 'score': 30, 'cause': 'Feux de forêt'},
    'etats unis': {'lat': 37.09, 'lon': -95.71, 'score': 50, 'cause': 'Risques multiples'},
    'antarctique': {'lat': -82.86, 'lon': 135.00, 'score': 100, 'cause': 'Fonte Inéluctable'},
    'australie': {'lat': -25.27, 'lon': 133.77, 'score': 80, 'cause': 'Incendies géants'}
}

def get_info_pays(destination):
    nom = str(destination).lower().strip()
    # Recherche dans la base (avec gestion des alias simples)
    for key in WORLD_CLIMATE_DATA:
        if key in nom: return WORLD_CLIMATE_DATA[key]
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Inconnu'}

# ==============================================================================
# 2. BARRE LATÉRALE : UPLOAD DU FICHIER
# ==============================================================================
st.sidebar.header("📂 Import des flux")
uploaded_file = st.sidebar.file_uploader("Chargez votre fichier 'Donnees_Consolidees_Voyageurs_2025.xlsx'", type=["xlsx"])

df = None
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.sidebar.success("✅ Fichier chargé !")
else:
    # Charge le fichier par défaut s'il existe
    try:
        df = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
        st.sidebar.info("ℹ️ Mode Démo : Données 2025 chargées.")
    except:
        st.sidebar.warning("⚠️ En attente de fichier...")

# ==============================================================================
# 3. AFFICHAGE DE LA CARTE DES RISQUES
# ==============================================================================
st.title("🗺️ Projet 3 : Cartographie des Risques Climatiques")
st.markdown("Cette interface analyse l'exposition de vos flux de voyageurs face aux risques physiques du réchauffement.")

if df is not None:
    # Vérification des colonnes
    if 'Destination' in df.columns and 'Pax' in df.columns:
        
        # Enrichissement automatique
        coords = df['Destination'].apply(lambda x: pd.Series(get_info_pays(x)))
        df_display = pd.concat([df, coords], axis=1).dropna(subset=['lat'])
        
        # KPIs de la carte
        c1, c2, c3 = st.columns(3)
        pax_total = df_display['Pax'].sum()
        pax_danger = df_display[df_display['score'] > 80]['Pax'].sum()
        
        c1.metric("Destinations identifiées", len(df_display['Destination'].unique()))
        c2.metric("Total Passagers", f"{pax_total:,.0f}")
        c3.metric("Exposition Risque Haut", f"{(pax_danger/pax_total)*100:.1f}%", delta="Score > 80", delta_color="inverse")

        st.divider()

        # LA CARTE
        fig = px.scatter_geo(
            df_display, lat="lat", lon="lon", size="Pax", color="score",
            hover_name="Destination", hover_data={"cause": True, "score": True, "Pax": True},
            color_continuous_scale=["#27ae60", "#f1c40f", "#c0392b"], # Vert -> Jaune -> Rouge
            range_color=[0, 100], projection="natural earth",
            title="Niveau de Vulnérabilité des Destinations"
        )
        
        fig.update_geos(showcountries=True, countrycolor="#ecf0f1", landcolor="#ffffff")
        fig.update_layout(height=650, margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

        # TABLEAUX D'ALERTE
        col_list1, col_list2 = st.columns(2)
        with col_list1:
            st.error("🚨 Top 5 Destinations en Péril")
            st.dataframe(df_display[df_display['score'] > 80].groupby(['Destination', 'cause'])['Pax'].sum().sort_values(ascending=False).head(5))
        with col_list2:
            st.success("🛡️ Top 5 Destinations 'Refuges'")
            st.dataframe(df_display[df_display['score'] < 30].groupby(['Destination', 'cause'])['Pax'].sum().sort_values(ascending=False).head(5))
            
    else:
        st.error("⚠️ Le fichier Excel doit contenir les colonnes 'Destination' et 'Pax'.")
else:
    st.info("Veuillez charger un fichier Excel dans la barre latérale pour commencer l'analyse.")
