import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==============================================================================
# 1. CONFIGURATION & DONNÉES CLIMATIQUES
# ==============================================================================
st.set_page_config(page_title="Climate Strategy Cockpit", layout="wide", page_icon="🌍")

# Base de connaissances (190+ pays) avec info Hémisphère pour la saisonnalité
# 'hem': 'N' (Nord) ou 'S' (Sud) -> Sert à calculer quand c'est l'été
WORLD_CLIMATE_DATA = {
    'afrique du sud': {'lat': -30.55, 'lon': 22.93, 'score': 70, 'cause': 'Stress Hydrique', 'hem': 'S'},
    'maroc': {'lat': 31.79, 'lon': -7.09, 'score': 85, 'cause': 'Stress Hydrique Critique', 'hem': 'N'},
    'egypte': {'lat': 26.82, 'lon': 30.80, 'score': 95, 'cause': 'Chaleur & Montée eaux', 'hem': 'N'},
    'tanzanie': {'lat': -6.36, 'lon': 34.88, 'score': 65, 'cause': 'Impact Kilimandjaro', 'hem': 'S'},
    'cap vert': {'lat': 16.53, 'lon': -23.04, 'score': 75, 'cause': 'Aridité & Ouragans', 'hem': 'N'},
    'namibie': {'lat': -22.95, 'lon': 18.49, 'score': 85, 'cause': 'Désertification', 'hem': 'S'},
    'madagascar': {'lat': -18.76, 'lon': 46.86, 'score': 80, 'cause': 'Cyclones', 'hem': 'S'},
    'vietnam': {'lat': 14.05, 'lon': 108.27, 'score': 80, 'cause': 'Submersion Delta', 'hem': 'N'},
    'indonesie': {'lat': -0.78, 'lon': 113.92, 'score': 80, 'cause': 'Montée eaux', 'hem': 'N'},
    'japon': {'lat': 36.20, 'lon': 138.25, 'score': 40, 'cause': 'Typhons', 'hem': 'N'},
    'nepal': {'lat': 28.39, 'lon': 84.12, 'score': 80, 'cause': 'Fonte Glaciers', 'hem': 'N'},
    'spitzberg': {'lat': 78.22, 'lon': 15.65, 'score': 98, 'cause': 'Réchauffement x4', 'hem': 'N'},
    'norvege': {'lat': 60.47, 'lon': 8.46, 'score': 15, 'cause': 'Refuge', 'hem': 'N'},
    'islande': {'lat': 64.96, 'lon': -19.02, 'score': 25, 'cause': 'Refuge / Fonte', 'hem': 'N'},
    'italie': {'lat': 41.87, 'lon': 12.56, 'score': 80, 'cause': 'Canicules', 'hem': 'N'},
    'grece': {'lat': 39.07, 'lon': 21.82, 'score': 85, 'cause': 'Incendies', 'hem': 'N'},
    'espagne': {'lat': 40.46, 'lon': -3.74, 'score': 85, 'cause': 'Désertification', 'hem': 'N'},
    'france': {'lat': 46.22, 'lon': 2.21, 'score': 40, 'cause': 'Sécheresse Sud', 'hem': 'N'},
    'perou': {'lat': -9.19, 'lon': -75.01, 'score': 75, 'cause': 'Fonte Glaciers Andins', 'hem': 'S'},
    'bresil': {'lat': -14.23, 'lon': -51.92, 'score': 60, 'cause': 'Déforestation', 'hem': 'S'},
    'canada': {'lat': 56.13, 'lon': -106.34, 'score': 30, 'cause': 'Feux de forêt', 'hem': 'N'},
    'etats unis': {'lat': 37.09, 'lon': -95.71, 'score': 50, 'cause': 'Risques multiples', 'hem': 'N'},
    'antarctique': {'lat': -82.86, 'lon': 135.00, 'score': 100, 'cause': 'Fonte Inéluctable', 'hem': 'S'},
    'australie': {'lat': -25.27, 'lon': 133.77, 'score': 80, 'cause': 'Incendies géants', 'hem': 'S'},
    'thailande': {'lat': 15.87, 'lon': 100.99, 'score': 70, 'cause': 'Inondations Bangkok', 'hem': 'N'},
    'mexique': {'lat': 23.63, 'lon': -102.55, 'score': 70, 'cause': 'Stress Hydrique', 'hem': 'N'},
    'royaume uni': {'lat': 55.37, 'lon': -3.43, 'score': 25, 'cause': 'Refuge relatif', 'hem': 'N'},
    'irlande': {'lat': 53.14, 'lon': -7.69, 'score': 20, 'cause': 'Refuge', 'hem': 'N'}
}

def get_info_pays(destination):
    nom = str(destination).lower().strip()
    alias = {'usa': 'etats unis', 'uk': 'royaume uni', 'morocco': 'maroc', 'egypt': 'egypte', 'south africa': 'afrique du sud', 'spain': 'espagne', 'italy': 'italie', 'greece': 'grece', 'turkey': 'turquie'}
    for k, v in alias.items():
        if k in nom: nom = v
    for key in WORLD_CLIMATE_DATA:
        if key in nom: return WORLD_CLIMATE_DATA[key]
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Inconnu', 'hem': 'N'}

def calculer_score_mensuel(base_score, cause, hemisphere, mois):
    """
    Simule la variation du risque selon la saison.
    En été : Risque Canicule/Sécheresse augmente (+15 points).
    En hiver : Risque diminue.
    """
    # Mois critiques (Été)
    if hemisphere == 'N':
        mois_chauds = [6, 7, 8] # Juin-Aout
    else:
        mois_chauds = [12, 1, 2] # Dec-Fev
        
    score_final = base_score
    
    # Si c'est un risque lié à la chaleur/feu/eau et qu'on est en été
    if any(x in cause.lower() for x in ['chaleur', 'sécheresse', 'incendie', 'hydrique', 'aridité']):
        if mois in mois_chauds:
            score_final += 15 # BOOM, ça devient rouge
        else:
            score_final -= 10 # Ça se calme en hiver
            
    return min(100, max(0, score_final)) # On borne entre 0 et 100

# ==============================================================================
# 2. INTERFACE & SIDEBAR
# ==============================================================================
st.sidebar.header("🎛️ Pilotage Temporel")

# UPLOAD
uploaded_file = st.sidebar.file_uploader("📂 Données Voyageurs", type=["xlsx"])
df_raw = None

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
else:
    try:
        df_raw = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
        st.sidebar.info("ℹ️ Mode Démo")
    except:
        pass

# SLIDERS STRATÉGIQUES
mois_select = st.sidebar.select_slider("📅 Mois de départ", options=range(1, 13), value=1, format_func=lambda x: pd.to_datetime(f"2025-{x}-01").strftime('%B'))
scenario = st.sidebar.radio("🔥 Scénario Climatique", ["Actuel (+1.2°C)", "Pessimiste (+4°C)"])
bonus_risk = 0 if "Actuel" in scenario else 20 # Si scénario +4°C, on ajoute 20 points de risque partout

# ==============================================================================
# 3. TRAITEMENT INTELLIGENT
# ==============================================================================
if df_raw is not None and 'Destination' in df_raw.columns:
    # 1. Enrichissement Géographique
    coords = df_raw['Destination'].apply(lambda x: pd.Series(get_info_pays(x)))
    df_full = pd.concat([df_raw, coords], axis=1).dropna(subset=['lat'])
    
    # 2. Calcul du Score Dynamique (Selon le mois choisi)
    df_full['score_mensuel'] = df_full.apply(
        lambda row: calculer_score_mensuel(row['score'], row['cause'], row['hem'], mois_select) + bonus_risk, 
        axis=1
    )
    df_full['score_mensuel'] = df_full['score_mensuel'].clip(0, 100) # Garde entre 0 et 100
    
    # 3. Agrégation (Pour la fluidité)
    df_agg = df_full.groupby(['Destination', 'lat', 'lon', 'cause'])[['Pax', 'score_mensuel']].agg({'Pax': 'sum', 'score_mensuel': 'mean'}).reset_index()

else:
    df_agg = None

# ==============================================================================
# 4. DASHBOARD VISUEL
# ==============================================================================
st.title("🌍 Strategic Climate Monitor 3.0")

if df_agg is not None:
    
    # --- A. KPI DYNAMIQUES (Changent avec le slider mois) ---
    col1, col2, col3 = st.columns(3)
    pax_risk_mois = df_agg[df_agg['score_mensuel'] > 80]['Pax'].sum()
    total_pax = df_agg['Pax'].sum()
    
    col1.metric("Mois Analysé", pd.to_datetime(f"2025-{mois_select}-01").strftime('%B'), "Saisonnalité active")
    col2.metric("Cash-at-Risk (Ce mois)", f"{(pax_risk_mois * 1500 / 1000000):.1f} M€", "Basé sur panier moyen 1.5k€")
    col3.metric("Part du Business Menacée", f"{(pax_risk_mois/total_pax)*100:.1f}%", delta_color="inverse")

    # --- B. LE GLOBE TERRESTRE 3D (WOUAH EFFECT) ---
    st.markdown("### 🌐 Visualisation Globale")
    
    fig = px.scatter_geo(
        df_agg, 
        lat="lat", lon="lon", 
        size="Pax", 
        color="score_mensuel",
        hover_name="Destination",
        hover_data={"cause": True, "score_mensuel": True, "Pax": True},
        color_continuous_scale=["#2ecc71", "#f1c40f", "#e74c3c", "#5e0000"], # Vert -> Jaune -> Rouge -> Noir
        range_color=[0, 100],
        projection="orthographic", # C'est ça qui fait le Globe !
        title=f"Exposition Mondiale - {pd.to_datetime(f'2025-{mois_select}-01').strftime('%B')}"
    )
    
    fig.update_geos(
        showcountries=True, countrycolor="#888888",
        showcoastlines=True, coastlinecolor="#333333",
        showocean=True, oceancolor="#090a14", # Océan sombre style NASA
        showland=True, landcolor="#1c1e26",   # Terre sombre
        bgcolor="#0e1117" # Fond de l'app
    )
    fig.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor="#0e1117", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # --- C. LE "TRAVEL SWITCHER" (ACTION PLAN) ---
    st.divider()
    st.subheader("💡 Recommandation Stratégique (IA)")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        # Liste des destinations rouges CE MOIS-CI
        dest_critiques = df_agg[df_agg['score_mensuel'] > 75]['Destination'].unique()
        if len(dest_critiques) > 0:
            choix_dest = st.selectbox("Destination à remplacer :", dest_critiques)
            info_dest = df_agg[df_agg['Destination'] == choix_dest].iloc[0]
            st.warning(f"⚠️ **{choix_dest}** est critique en {pd.to_datetime(f'2025-{mois_select}-01').strftime('%B')}.")
            st.write(f"Cause : {info_dest['cause']}")
        else:
            st.success("Aucune destination critique ce mois-ci !")
            choix_dest = None

    with c2:
        if choix_dest:
            # Chercher une alternative verte
            alt = df_agg[df_agg['score_mensuel'] < 40].sort_values('score_mensuel')
            if not alt.empty:
                best = alt.iloc[0]
                st.success(f"✅ Alternative Suggérée : **{best['Destination']}**")
                st.write(f"En redirigeant les flux, vous économisez **{info_dest['score_mensuel'] - best['score_mensuel']:.0f} points de risque**.")
                
                # Graphique comparatif simple
                chart_data = pd.DataFrame({
                    "Destination": [choix_dest, best['Destination']],
                    "Risque": [info_dest['score_mensuel'], best['score_mensuel']],
                    "Color": ["Rouge", "Vert"]
                })
                st.bar_chart(chart_data.set_index("Destination")['Risque'], color=["#ff0000", "#00ff00"]) # Simple chart

else:
    st.info("👋 Bonjour ! Chargez votre fichier Excel à gauche pour générer le Globe.")
