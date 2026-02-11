import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 🧩 LE "CERVEAU" MONDIAL (DATABASE INTÉGRÉE)
# ==============================================================================
# Cette base couvre le monde entier. Plus besoin de fichier externe.
WORLD_CLIMATE_DATA = {
    # --- AFRIQUE (Vulnérabilité: Très Haute - Sécheresse & Chaleur) ---
    'afrique du sud': {'lat': -30.55, 'lon': 22.93, 'score': 70, 'cause': 'Stress Hydrique (Day Zero)'},
    'algerie': {'lat': 28.03, 'lon': 1.65, 'score': 85, 'cause': 'Canicules & Sécheresse'},
    'angola': {'lat': -11.20, 'lon': 17.87, 'score': 65, 'cause': 'Sécheresse Sud & Inondations'},
    'benin': {'lat': 9.30, 'lon': 2.31, 'score': 60, 'cause': 'Érosion côtière'},
    'botswana': {'lat': -22.32, 'lon': 24.68, 'score': 80, 'cause': 'Désertification (Kalahari)'},
    'burkina faso': {'lat': 12.23, 'lon': -1.56, 'score': 80, 'cause': 'Avancée du désert'},
    'cameroun': {'lat': 7.36, 'lon': 12.35, 'score': 60, 'cause': 'Déforestation'},
    'cap vert': {'lat': 16.53, 'lon': -23.04, 'score': 75, 'cause': 'Aridité & Ouragans'},
    'congo': {'lat': -0.22, 'lon': 15.82, 'score': 55, 'cause': 'Déforestation'},
    'cote d ivoire': {'lat': 7.54, 'lon': -5.54, 'score': 60, 'cause': 'Érosion côtière'},
    'egypte': {'lat': 26.82, 'lon': 30.80, 'score': 95, 'cause': 'Montée eaux (Delta) & Chaleur'},
    'ethiopie': {'lat': 9.14, 'lon': 40.48, 'score': 75, 'cause': 'Sécheresse chronique'},
    'gabon': {'lat': -0.80, 'lon': 11.60, 'score': 50, 'cause': 'Impact modéré'},
    'ghana': {'lat': 7.94, 'lon': -1.02, 'score': 60, 'cause': 'Érosion côtière'},
    'kenya': {'lat': -0.02, 'lon': 37.90, 'score': 70, 'cause': 'Saisons des pluies instables'},
    'madagascar': {'lat': -18.76, 'lon': 46.86, 'score': 80, 'cause': 'Cyclones & Sécheresse Sud'},
    'maroc': {'lat': 31.79, 'lon': -7.09, 'score': 85, 'cause': 'Stress Hydrique Critique'},
    'maurice': {'lat': -20.34, 'lon': 57.55, 'score': 70, 'cause': 'Érosion & Coraux'},
    'mauritanie': {'lat': 21.00, 'lon': -10.94, 'score': 90, 'cause': 'Hyper-aridité'},
    'mozambique': {'lat': -18.66, 'lon': 35.52, 'score': 80, 'cause': 'Cyclones intenses'},
    'namibie': {'lat': -22.95, 'lon': 18.49, 'score': 85, 'cause': 'Désertification'},
    'nigeria': {'lat': 9.08, 'lon': 8.67, 'score': 70, 'cause': 'Chaleur humide & Inondations'},
    'ouganda': {'lat': 1.37, 'lon': 32.29, 'score': 60, 'cause': 'Agriculture menacée'},
    'reunion': {'lat': -21.11, 'lon': 55.53, 'score': 65, 'cause': 'Cyclones Tropicaux'},
    'rwanda': {'lat': -1.94, 'lon': 29.87, 'score': 55, 'cause': 'Érosion des sols'},
    'senegal': {'lat': 14.49, 'lon': -14.45, 'score': 80, 'cause': 'Montée des eaux (St Louis)'},
    'seychelles': {'lat': -4.67, 'lon': 55.49, 'score': 85, 'cause': 'Submersion marine'},
    'soudan': {'lat': 12.86, 'lon': 30.21, 'score': 95, 'cause': 'Inhabitable (Chaleur)'},
    'tanzanie': {'lat': -6.36, 'lon': 34.88, 'score': 65, 'cause': 'Impact Kilimandjaro & Sécheresse'},
    'tchad': {'lat': 15.45, 'lon': 18.73, 'score': 90, 'cause': 'Assèchement Lac Tchad'},
    'togo': {'lat': 8.61, 'lon': 0.82, 'score': 60, 'cause': 'Érosion côtière'},
    'tunisie': {'lat': 33.88, 'lon': 9.53, 'score': 85, 'cause': 'Sécheresse & Tourisme'},
    'zambie': {'lat': -13.13, 'lon': 27.84, 'score': 70, 'cause': 'Chute débit Victoria Falls'},
    'zimbabwe': {'lat': -19.01, 'lon': 29.15, 'score': 75, 'cause': 'Sécheresse extrême'},

    # --- ASIE (Vulnérabilité: Haute - Moussons & Glaciers) ---
    'afghanistan': {'lat': 33.93, 'lon': 67.70, 'score': 80, 'cause': 'Sécheresse & Instabilité'},
    'arabie saoudite': {'lat': 23.88, 'lon': 45.07, 'score': 90, 'cause': 'Chaleur Extrême'},
    'armenie': {'lat': 40.06, 'lon': 45.03, 'score': 55, 'cause': 'Désertification'},
    'azerbaidjan': {'lat': 40.14, 'lon': 47.57, 'score': 60, 'cause': 'Baisse niveau Caspienne'},
    'bangladesh': {'lat': 23.68, 'lon': 90.35, 'score': 95, 'cause': 'Submersion majeure'},
    'birmanie': {'lat': 21.91, 'lon': 95.95, 'score': 75, 'cause': 'Cyclones'},
    'cambodge': {'lat': 12.56, 'lon': 104.99, 'score': 75, 'cause': 'Crues Mékong'},
    'chine': {'lat': 35.86, 'lon': 104.19, 'score': 65, 'cause': 'Pollution & Désertification'},
    'coree du sud': {'lat': 35.90, 'lon': 127.76, 'score': 45, 'cause': 'Typhons'},
    'emirats arabes unis': {'lat': 23.42, 'lon': 53.84, 'score': 90, 'cause': 'Chaleur Humide'},
    'georgie': {'lat': 42.31, 'lon': 43.35, 'score': 50, 'cause': 'Fonte glaciers Caucase'},
    'inde': {'lat': 20.59, 'lon': 78.96, 'score': 85, 'cause': 'Vagues chaleur mortelles'},
    'indonesie': {'lat': -0.78, 'lon': 113.92, 'score': 80, 'cause': 'Montée eaux (Jakarta)'},
    'irak': {'lat': 33.22, 'lon': 43.67, 'score': 90, 'cause': 'Pénurie Eau (Tigre/Euphrate)'},
    'iran': {'lat': 32.42, 'lon': 53.68, 'score': 85, 'cause': 'Assèchement complet'},
    'israel': {'lat': 31.04, 'lon': 34.85, 'score': 75, 'cause': 'Stress Hydrique'},
    'japon': {'lat': 36.20, 'lon': 138.25, 'score': 40, 'cause': 'Typhons & Vieillissement'},
    'jordanie': {'lat': 30.58, 'lon': 36.23, 'score': 90, 'cause': 'Pénurie Eau Critique'},
    'kazakhstan': {'lat': 48.01, 'lon': 66.92, 'score': 60, 'cause': 'Climat continental extrême'},
    'kirghizistan': {'lat': 41.20, 'lon': 74.76, 'score': 65, 'cause': 'Fonte glaciers Tian Shan'},
    'laos': {'lat': 19.85, 'lon': 102.49, 'score': 65, 'cause': 'Déforestation'},
    'liban': {'lat': 33.85, 'lon': 35.86, 'score': 70, 'cause': 'Incendies & Eau'},
    'malaisie': {'lat': 4.21, 'lon': 101.97, 'score': 60, 'cause': 'Chaleur & Humidité'},
    'maldives': {'lat': 3.20, 'lon': 73.22, 'score': 98, 'cause': 'Disparition (Montée eaux)'},
    'mongolie': {'lat': 46.86, 'lon': 103.84, 'score': 70, 'cause': 'Dzud (Hiver extrême)'},
    'nepal': {'lat': 28.39, 'lon': 84.12, 'score': 80, 'cause': 'Fonte Glaciers Himalaya'},
    'oman': {'lat': 21.47, 'lon': 55.97, 'score': 90, 'cause': 'Invivable en été'},
    'ouzbekistan': {'lat': 41.37, 'lon': 64.58, 'score': 80, 'cause': 'Assèchement Aral'},
    'pakistan': {'lat': 30.37, 'lon': 69.34, 'score': 90, 'cause': 'Inondations monstres & Chaleur'},
    'philippines': {'lat': 12.87, 'lon': 121.77, 'score': 85, 'cause': 'Super-Typhons'},
    'sri lanka': {'lat': 7.87, 'lon': 80.77, 'score': 70, 'cause': 'Érosion & Moussons'},
    'syrie': {'lat': 34.80, 'lon': 38.99, 'score': 90, 'cause': 'Sécheresse historique'},
    'tadjikistan': {'lat': 38.86, 'lon': 71.27, 'score': 70, 'cause': 'Fonte glaciers Pamir'},
    'taiwan': {'lat': 23.69, 'lon': 120.96, 'score': 55, 'cause': 'Typhons'},
    'thailande': {'lat': 15.87, 'lon': 100.99, 'score': 70, 'cause': 'Inondations Bangkok'},
    'turquie': {'lat': 38.96, 'lon': 35.24, 'score': 75, 'cause': 'Sécheresse Anatolie'},
    'vietnam': {'lat': 14.05, 'lon': 108.27, 'score': 80, 'cause': 'Submersion Delta Mékong'},
    'yemen': {'lat': 15.55, 'lon': 48.51, 'score': 95, 'cause': 'Crise humanitaire & Eau'},

    # --- EUROPE (Vulnérabilité: Moyenne - Sud exposé, Nord refuge) ---
    'albanie': {'lat': 41.15, 'lon': 20.16, 'score': 60, 'cause': 'Impact Méditerranéen'},
    'allemagne': {'lat': 51.16, 'lon': 10.45, 'score': 30, 'cause': 'Inondations fluviales'},
    'autriche': {'lat': 47.51, 'lon': 14.55, 'score': 35, 'cause': 'Moins de neige (Ski)'},
    'belgique': {'lat': 50.50, 'lon': 4.46, 'score': 30, 'cause': 'Canicules urbaines'},
    'bulgarie': {'lat': 42.73, 'lon': 25.48, 'score': 55, 'cause': 'Sécheresse'},
    'chypre': {'lat': 35.12, 'lon': 33.42, 'score': 85, 'cause': 'Désertification'},
    'croatie': {'lat': 45.10, 'lon': 15.20, 'score': 60, 'cause': 'Feux de forêt'},
    'danemark': {'lat': 56.26, 'lon': 9.50, 'score': 25, 'cause': 'Montée des eaux'},
    'espagne': {'lat': 40.46, 'lon': -3.74, 'score': 85, 'cause': 'Désertification massive'},
    'finlande': {'lat': 61.92, 'lon': 25.74, 'score': 15, 'cause': 'Zone Refuge (Froid)'},
    'france': {'lat': 46.22, 'lon': 2.21, 'score': 40, 'cause': 'Sécheresse Sud & Canicules'},
    'grece': {'lat': 39.07, 'lon': 21.82, 'score': 85, 'cause': 'Incendies incontrôlables'},
    'hongrie': {'lat': 47.16, 'lon': 19.50, 'score': 50, 'cause': 'Vagues de chaleur'},
    'irlande': {'lat': 53.14, 'lon': -7.69, 'score': 20, 'cause': 'Zone Refuge'},
    'islande': {'lat': 64.96, 'lon': -19.02, 'score': 25, 'cause': 'Fonte Glaciers / Refuge'},
    'italie': {'lat': 41.87, 'lon': 12.56, 'score': 80, 'cause': 'Canicules & Sécheresse Pô'},
    'malte': {'lat': 35.93, 'lon': 14.37, 'score': 85, 'cause': 'Pénurie Eau'},
    'montenegro': {'lat': 42.70, 'lon': 19.37, 'score': 60, 'cause': 'Feux de forêt'},
    'norvege': {'lat': 60.47, 'lon': 8.46, 'score': 15, 'cause': 'Zone Refuge'},
    'pays bas': {'lat': 52.13, 'lon': 5.29, 'score': 45, 'cause': 'Submersion (Digues)'},
    'pologne': {'lat': 51.91, 'lon': 19.14, 'score': 30, 'cause': 'Sécheresse agricole'},
    'portugal': {'lat': 39.39, 'lon': -8.22, 'score': 80, 'cause': 'Incendies géants'},
    'roumanie': {'lat': 45.94, 'lon': 24.96, 'score': 50, 'cause': 'Saisons marquées'},
    'royaume uni': {'lat': 55.37, 'lon': -3.43, 'score': 25, 'cause': 'Zone Refuge Relative'},
    'russie': {'lat': 61.52, 'lon': 105.31, 'score': 40, 'cause': 'Fonte Permafrost'},
    'slovenie': {'lat': 46.15, 'lon': 14.99, 'score': 40, 'cause': 'Inondations'},
    'suede': {'lat': 60.12, 'lon': 18.64, 'score': 15, 'cause': 'Zone Refuge'},
    'suisse': {'lat': 46.81, 'lon': 8.22, 'score': 35, 'cause': 'Disparition glaciers'},
    'ukraine': {'lat': 48.37, 'lon': 31.16, 'score': 40, 'cause': 'Sécheresse'},

    # --- AMERIQUES (Vulnérabilité: Mixte - Ouragans & Andes) ---
    'argentine': {'lat': -38.41, 'lon': -63.61, 'score': 50, 'cause': 'Sécheresse Pampas'},
    'belize': {'lat': 17.18, 'lon': -88.49, 'score': 75, 'cause': 'Ouragans & Coraux'},
    'bolivie': {'lat': -16.29, 'lon': -63.58, 'score': 65, 'cause': 'Disparition Lacs'},
    'bresil': {'lat': -14.23, 'lon': -51.92, 'score': 60, 'cause': 'Déforestation Amazonie'},
    'canada': {'lat': 56.13, 'lon': -106.34, 'score': 30, 'cause': 'Feux de forêt (mais Refuge)'},
    'chili': {'lat': -35.67, 'lon': -71.54, 'score': 70, 'cause': 'Méga-Sécheresse'},
    'colombie': {'lat': 4.57, 'lon': -74.29, 'score': 55, 'cause': 'Glissements terrain'},
    'costa rica': {'lat': 9.74, 'lon': -83.75, 'score': 50, 'cause': 'Biodiversité menacée'},
    'cuba': {'lat': 21.52, 'lon': -77.78, 'score': 80, 'cause': 'Ouragans majeurs'},
    'equateur': {'lat': -1.83, 'lon': -78.18, 'score': 60, 'cause': 'El Niño extrême'},
    'etats unis': {'lat': 37.09, 'lon': -95.71, 'score': 50, 'cause': 'Risques multiples (Feux/Hurricanes)'},
    'guatemala': {'lat': 15.78, 'lon': -90.23, 'score': 70, 'cause': 'Sécheresse corridor sec'},
    'mexique': {'lat': 23.63, 'lon': -102.55, 'score': 70, 'cause': 'Stress Hydrique'},
    'nicaragua': {'lat': 12.86, 'lon': -85.20, 'score': 75, 'cause': 'Ouragans'},
    'panama': {'lat': 8.53, 'lon': -80.78, 'score': 60, 'cause': 'Manque eau Canal'},
    'perou': {'lat': -9.19, 'lon': -75.01, 'score': 75, 'cause': 'Fonte Glaciers Andins'},
    'uruguay': {'lat': -32.52, 'lon': -55.76, 'score': 40, 'cause': 'Inondations'},
    'venezuela': {'lat': 6.42, 'lon': -66.58, 'score': 60, 'cause': 'Instabilité climat'},

    # --- OCÉANIE & POLES ---
    'australie': {'lat': -25.27, 'lon': 133.77, 'score': 80, 'cause': 'Incendies géants'},
    'fidji': {'lat': -17.71, 'lon': 178.06, 'score': 85, 'cause': 'Montée des eaux'},
    'nouvelle zelande': {'lat': -40.90, 'lon': 174.88, 'score': 30, 'cause': 'Zone Refuge'},
    'papouasie nouvelle guinee': {'lat': -6.31, 'lon': 143.95, 'score': 70, 'cause': 'Disparition îles'},
    'polynesie': {'lat': -17.67, 'lon': -149.40, 'score': 85, 'cause': 'Submersion Atolls'},
    'antarctique': {'lat': -82.86, 'lon': 135.00, 'score': 100, 'cause': 'Fonte Inéluctable'},
    'groenland': {'lat': 71.70, 'lon': -42.60, 'score': 95, 'cause': 'Point de Bascule'},
    'spitzberg': {'lat': 78.22, 'lon': 15.65, 'score': 98, 'cause': 'Réchauffement x4'}
}

# --- FONCTION DE NORMALISATION INTELLIGENTE ---
def get_info_pays(destination):
    """Trouve le pays dans la base, peu importe comment il est écrit."""
    nom = str(destination).lower().strip()
    
    # 1. Alias pour comprendre les variantes
    alias = {
        'usa': 'etats unis', 'us': 'etats unis', 'united states': 'etats unis',
        'uk': 'royaume uni', 'great britain': 'royaume uni', 'angleterre': 'royaume uni', 'ecosse': 'royaume uni',
        'morocco': 'maroc', 'egypt': 'egypte', 'spain': 'espagne', 'italy': 'italie',
        'greece': 'grece', 'turkey': 'turquie', 'south africa': 'afrique du sud',
        'burma': 'birmanie', 'myanmar': 'birmanie', 'viet nam': 'vietnam',
        'cabo verde': 'cap vert', 'nz': 'nouvelle zelande',
        'hollande': 'pays bas', 'netherlands': 'pays bas', 'deutschland': 'allemagne'
    }
    
    # Suppression des accents pour la recherche
    for char, repl in {'é':'e', 'è':'e', 'ê':'e', 'ï':'i', 'î':'i', 'ô':'o'}.items():
        nom = nom.replace(char, repl)
    
    if nom in alias:
        nom = alias[nom]
        
    # 2. Recherche dans la base
    if nom in WORLD_CLIMATE_DATA:
        return WORLD_CLIMATE_DATA[nom]
    
    # 3. Fallback (Si non trouvé)
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Donnée manquante'}

# --- INTERFACE STREAMLIT ---
st.header("🌍 Carte des Risques (Base Mondiale Intégrée)")
st.markdown("Analyse basée sur une base de données interne de **190+ territoires**.")

try:
    # 1. CHARGEMENT
    df = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
    
    # 2. ENRICHISSEMENT (Application du Cerveau Mondial)
    # On crée 4 nouvelles colonnes d'un coup
    df_enriched = df.copy()
    
    # On applique la fonction ligne par ligne
    def enrichir_ligne(dest):
        info = get_info_pays(dest)
        return pd.Series([info['lat'], info['lon'], info['score'], info['cause']])

    df_enriched[['lat', 'lon', 'Score_Vulnérabilité', 'Cause_Risque']] = df_enriched['Destination'].apply(enrichir_ligne)
    
    # On ne garde que ce qui a été trouvé
    df_map = df_enriched.dropna(subset=['lat'])
    
    # 3. STATS DE COUVERTURE
    couverture = (len(df_map) / len(df)) * 100
    if couverture < 100:
        st.caption(f"ℹ️ Couverture de la base : {couverture:.1f}% des voyages ont été géolocalisés.")

    # 4. CARTE FINALE
    fig = px.scatter_geo(
        df_map,
        lat="lat", lon="lon",
        color="Score_Vulnérabilité",
        size="Pax",
        hover_name="Destination",
        hover_data={"Cause_Risque": True, "Score_Vulnérabilité": True, "lat": False, "lon": False},
        projection="natural earth",
        color_continuous_scale=["#27ae60", "#f1c40f", "#c0392b"], # Vert -> Jaune -> Rouge
        range_color=[0, 100],
        title=f"Exposition Climatique ({len(df_map['Destination'].unique())} destinations analysées)"
    )
    
    fig.update_geos(showcountries=True, countrycolor="#ecf0f1", landcolor="#ffffff")
    fig.update_layout(height=650, margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. LISTE ROUGE
    st.subheader("🚨 Zones d'Alerte (Score > 75)")
    risk_zones = df_map[df_map['Score_Vulnérabilité'] > 75].groupby('Destination').agg({'Pax': 'sum', 'Cause_Risque': 'first'}).sort_values('Pax', ascending=False).head(8)
    st.table(risk_zones)

except FileNotFoundError:
    st.error("Fichier 'Donnees_Consolidees_Voyageurs_2025.xlsx' manquant.")