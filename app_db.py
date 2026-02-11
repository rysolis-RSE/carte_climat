import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURATION & INTELLIGENCE CLIMATIQUE (DATA WAREHOUSE)
# ==============================================================================
st.set_page_config(page_title="Strategic Climate Cockpit", layout="wide", page_icon="🌍")

# Base de connaissances AVEC CONTINENTS pour la logique "à côté"
WORLD_CLIMATE_DATA = {
    # --- AFRIQUE ---
    'afrique du sud': {'lat': -30.55, 'lon': 22.93, 'score': 70, 'cause': 'Stress Hydrique', 'hem': 'S', 'region': 'Afrique'},
    'maroc': {'lat': 31.79, 'lon': -7.09, 'score': 85, 'cause': 'Stress Hydrique Critique', 'hem': 'N', 'region': 'Afrique'},
    'egypte': {'lat': 26.82, 'lon': 30.80, 'score': 95, 'cause': 'Chaleur & Montée eaux', 'hem': 'N', 'region': 'Afrique'},
    'tanzanie': {'lat': -6.36, 'lon': 34.88, 'score': 65, 'cause': 'Impact Kilimandjaro', 'hem': 'S', 'region': 'Afrique'},
    'cap vert': {'lat': 16.53, 'lon': -23.04, 'score': 75, 'cause': 'Aridité & Ouragans', 'hem': 'N', 'region': 'Afrique'},
    'namibie': {'lat': -22.95, 'lon': 18.49, 'score': 85, 'cause': 'Désertification', 'hem': 'S', 'region': 'Afrique'},
    'madagascar': {'lat': -18.76, 'lon': 46.86, 'score': 80, 'cause': 'Cyclones', 'hem': 'S', 'region': 'Afrique'},
    
    # --- ASIE ---
    'vietnam': {'lat': 14.05, 'lon': 108.27, 'score': 80, 'cause': 'Submersion Delta', 'hem': 'N', 'region': 'Asie'},
    'indonesie': {'lat': -0.78, 'lon': 113.92, 'score': 80, 'cause': 'Montée eaux', 'hem': 'N', 'region': 'Asie'},
    'japon': {'lat': 36.20, 'lon': 138.25, 'score': 40, 'cause': 'Typhons', 'hem': 'N', 'region': 'Asie'},
    'nepal': {'lat': 28.39, 'lon': 84.12, 'score': 80, 'cause': 'Fonte Glaciers', 'hem': 'N', 'region': 'Asie'},
    'sri lanka': {'lat': 7.87, 'lon': 80.77, 'score': 70, 'cause': 'Moussons', 'hem': 'N', 'region': 'Asie'},
    'thailande': {'lat': 15.87, 'lon': 100.99, 'score': 70, 'cause': 'Inondations Bangkok', 'hem': 'N', 'region': 'Asie'},
    
    # --- EUROPE (NORD & SUD) ---
    'spitzberg': {'lat': 78.22, 'lon': 15.65, 'score': 98, 'cause': 'Réchauffement x4', 'hem': 'N', 'region': 'Europe'},
    'norvege': {'lat': 60.47, 'lon': 8.46, 'score': 15, 'cause': 'Zone Refuge', 'hem': 'N', 'region': 'Europe'},
    'islande': {'lat': 64.96, 'lon': -19.02, 'score': 25, 'cause': 'Refuge / Fonte', 'hem': 'N', 'region': 'Europe'},
    'suede': {'lat': 60.12, 'lon': 18.64, 'score': 20, 'cause': 'Zone Refuge', 'hem': 'N', 'region': 'Europe'},
    'finlande': {'lat': 61.92, 'lon': 25.74, 'score': 20, 'cause': 'Zone Refuge', 'hem': 'N', 'region': 'Europe'},
    'royaume uni': {'lat': 55.37, 'lon': -3.43, 'score': 25, 'cause': 'Refuge relatif', 'hem': 'N', 'region': 'Europe'},
    'irlande': {'lat': 53.14, 'lon': -7.69, 'score': 20, 'cause': 'Refuge', 'hem': 'N', 'region': 'Europe'},
    'suisse': {'lat': 46.81, 'lon': 8.22, 'score': 35, 'cause': 'Refuge Alpin', 'hem': 'N', 'region': 'Europe'},
    'italie': {'lat': 41.87, 'lon': 12.56, 'score': 80, 'cause': 'Canicules', 'hem': 'N', 'region': 'Europe'},
    'grece': {'lat': 39.07, 'lon': 21.82, 'score': 85, 'cause': 'Incendies', 'hem': 'N', 'region': 'Europe'},
    'espagne': {'lat': 40.46, 'lon': -3.74, 'score': 85, 'cause': 'Désertification', 'hem': 'N', 'region': 'Europe'},
    'france': {'lat': 46.22, 'lon': 2.21, 'score': 40, 'cause': 'Sécheresse Sud', 'hem': 'N', 'region': 'Europe'},
    'croatie': {'lat': 45.10, 'lon': 15.20, 'score': 60, 'cause': 'Feux de forêt', 'hem': 'N', 'region': 'Europe'},
    
    # --- AMÉRIQUES ---
    'costa rica': {'lat': 9.74, 'lon': -83.75, 'score': 50, 'cause': 'Biodiversité', 'hem': 'N', 'region': 'Amériques'},
    'perou': {'lat': -9.19, 'lon': -75.01, 'score': 75, 'cause': 'Fonte Glaciers Andins', 'hem': 'S', 'region': 'Amériques'},
    'bresil': {'lat': -14.23, 'lon': -51.92, 'score': 60, 'cause': 'Déforestation', 'hem': 'S', 'region': 'Amériques'},
    'canada': {'lat': 56.13, 'lon': -106.34, 'score': 30, 'cause': 'Feux (mais Refuge)', 'hem': 'N', 'region': 'Amériques'},
    'etats unis': {'lat': 37.09, 'lon': -95.71, 'score': 50, 'cause': 'Risques multiples', 'hem': 'N', 'region': 'Amériques'},
    'mexique': {'lat': 23.63, 'lon': -102.55, 'score': 70, 'cause': 'Stress Hydrique', 'hem': 'N', 'region': 'Amériques'},
    'argentine': {'lat': -38.41, 'lon': -63.61, 'score': 45, 'cause': 'Patagonie Refuge', 'hem': 'S', 'region': 'Amériques'},
    
    # --- OCÉANIE & POLES ---
    'antarctique': {'lat': -82.86, 'lon': 135.00, 'score': 100, 'cause': 'Fonte Inéluctable', 'hem': 'S', 'region': 'Pôles'},
    'australie': {'lat': -25.27, 'lon': 133.77, 'score': 80, 'cause': 'Incendies géants', 'hem': 'S', 'region': 'Océanie'},
    'nouvelle zelande': {'lat': -40.90, 'lon': 174.88, 'score': 30, 'cause': 'Zone Refuge Australe', 'hem': 'S', 'region': 'Océanie'}
}

# --- FONCTIONS UTILITAIRES ---
def get_info_pays(destination):
    """Récupère infos géographiques + RÉGION"""
    nom = str(destination).lower().strip()
    alias = {
        'usa': 'etats unis', 'uk': 'royaume uni', 'morocco': 'maroc', 'egypt': 'egypte', 
        'south africa': 'afrique du sud', 'spain': 'espagne', 'italy': 'italie', 
        'greece': 'grece', 'turkey': 'turquie', 'burma': 'birmanie', 'nz': 'nouvelle zelande',
        'sweden': 'suede', 'finland': 'finlande', 'switzerland': 'suisse'
    }
    for k, v in alias.items():
        if k in nom: nom = v
    for key in WORLD_CLIMATE_DATA:
        if key in nom: return WORLD_CLIMATE_DATA[key]
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Inconnu', 'hem': 'N', 'region': 'Monde'}

def calculer_score_mensuel(base_score, cause, hemisphere, mois):
    """Ajuste le score selon la saison"""
    if hemisphere == 'N':
        mois_chauds = [6, 7, 8]
    else:
        mois_chauds = [12, 1, 2]
        
    score_final = base_score
    if any(x in str(cause).lower() for x in ['chaleur', 'sécheresse', 'incendie', 'hydrique', 'aridité']):
        if mois in mois_chauds:
            score_final += 15
        else:
            score_final -= 10
            
    return min(100, max(0, score_final))

# ==============================================================================
# 2. INPUTS
# ==============================================================================
st.sidebar.header("💶 Paramètres Financiers")
panier_moyen = st.sidebar.number_input("Panier Moyen par Client (€)", value=2500, step=100)
st.sidebar.divider()
st.sidebar.header("🎛️ Pilotage Temporel")

uploaded_file = st.sidebar.file_uploader("📂 Données Voyageurs (Excel)", type=["xlsx"])
df_raw = None

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
        st.sidebar.success("✅ Fichier chargé !")
    except:
        st.sidebar.error("Erreur fichier")
else:
    try:
        df_raw = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
        st.sidebar.info("ℹ️ Mode Démo (2025)")
    except:
        pass 

mois_select = st.sidebar.select_slider(
    "📅 Mois de départ", 
    options=range(1, 13), 
    value=7, 
    format_func=lambda x: pd.to_datetime(f"2025-{x}-01").strftime('%B')
)

scenario = st.sidebar.radio("🔥 Scénario Climatique", ["Actuel (+1.2°C)", "Pessimiste (+4°C)"])
bonus_risk = 0 if "Actuel" in scenario else 20 

# ==============================================================================
# 3. TRAITEMENT
# ==============================================================================
if df_raw is not None and 'Destination' in df_raw.columns:
    coords = df_raw['Destination'].apply(lambda x: pd.Series(get_info_pays(x)))
    df_full = pd.concat([df_raw, coords], axis=1).dropna(subset=['lat'])
    
    df_full['score_mensuel'] = df_full.apply(
        lambda row: calculer_score_mensuel(row['score'], row['cause'], row['hem'], mois_select) + bonus_risk, 
        axis=1
    )
    df_full['score_mensuel'] = df_full['score_mensuel'].clip(0, 100)
    
    if 'Pax' not in df_full.columns: df_full['Pax'] = 1
    df_full['Cash_at_Risk'] = df_full['Pax'] * panier_moyen
    
    # Agrégation (On ajoute 'region' au groupby)
    df_agg = df_full.groupby(['Destination', 'lat', 'lon', 'cause', 'region'])[['Pax', 'score_mensuel', 'Cash_at_Risk']].agg(
        {'Pax': 'sum', 'score_mensuel': 'mean', 'Cash_at_Risk': 'sum'}
    ).reset_index()

else:
    df_agg = None

# ==============================================================================
# 4. DASHBOARD
# ==============================================================================
st.title("🌍 Strategic Climate Cockpit")

if df_agg is not None:
    
    # KPI
    risk_high = df_agg[df_agg['score_mensuel'] > 75]
    cash_total = df_agg['Cash_at_Risk'].sum()
    cash_risk = risk_high['Cash_at_Risk'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("CA Analysé", f"{cash_total/1000000:.1f} M€")
    col2.metric("⚠️ CA Menacé", f"{cash_risk/1000000:.1f} M€", f"{(cash_risk/cash_total)*100:.1f}%", delta_color="inverse")
    col3.metric("Saison", pd.to_datetime(f"2025-{mois_select}-01").strftime('%B'))

    st.divider()

    # GLOBE 3D
    fig = px.scatter_geo(
        df_agg, lat="lat", lon="lon", size="Cash_at_Risk", color="score_mensuel",
        hover_name="Destination",
        hover_data={"cause": True, "score_mensuel": True, "Cash_at_Risk": ":.0f"},
        color_continuous_scale=["#2ecc71", "#f1c40f", "#e74c3c", "#5e0000"], 
        range_color=[0, 100], projection="orthographic", 
        title=f"Exposition Financière Monde - {pd.to_datetime(f'2025-{mois_select}-01').strftime('%B')}"
    )
    fig.update_geos(showcountries=True, countrycolor="#888888", showcoastlines=True, coastlinecolor="#333333", showocean=True, oceancolor="#090a14", showland=True, landcolor="#1c1e26", bgcolor="#0e1117")
    fig.update_layout(height=650, margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor="#0e1117", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # --- TRAVEL SWITCHER INTELLIGENT (Proximité) ---
    st.divider()
    st.subheader("💡 Action Plan : Alternatives Régionales")
    st.markdown("L'IA cherche d'abord **la destination sûre la plus proche** (même région).")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        # Destinations rouges
        dest_critiques = df_agg[df_agg['score_mensuel'] > 75].sort_values('Cash_at_Risk', ascending=False)
        liste_rouges = dest_critiques['Destination'].unique()
        
        if len(liste_rouges) > 0:
            choix_dest = st.selectbox("Sélectionner un marché à protéger :", liste_rouges)
            info_dest = df_agg[df_agg['Destination'] == choix_dest].iloc[0]
            region_actuelle = info_dest['region']
            
            st.error(f"🚨 **{choix_dest}**")
            st.caption(f"Région : {region_actuelle} | Cause : {info_dest['cause']}")
            st.metric("CA à Sécuriser", f"{info_dest['Cash_at_Risk']:,.0f} €")
        else:
            choix_dest = None
            st.success("✅ Aucun marché critique.")

    with c2:
        if choix_dest:
            # 1. Chercher dans la MÊME région, avec score faible (<50)
            alt_locale = df_agg[
                (df_agg['region'] == region_actuelle) & 
                (df_agg['score_mensuel'] < 50) & 
                (df_agg['Destination'] != choix_dest)
            ].sort_values('score_mensuel')
            
            # 2. Chercher dans le MONDE entier (Plan B)
            alt_global = df_agg[df_agg['score_mensuel'] < 40].sort_values('score_mensuel')
            
            best = None
            type_sol = ""
            
            if not alt_locale.empty:
                best = alt_locale.iloc[0] # La meilleure locale
                type_sol = f"✅ Solution Régionale ({region_actuelle})"
            elif not alt_global.empty:
                best = alt_global.iloc[0] # La meilleure mondiale (Fallback)
                type_sol = "🌍 Plan B (Aucune solution locale sûre)"
            
            if best is not None:
                st.success(f"{type_sol} : **{best['Destination']}**")
                st.markdown(f"Alternative la moins risquée située à proximité. Score : **{best['score_mensuel']:.0f}/100** ({best['cause']}).")
                
                # GRAPHIQUE
                chart_data = pd.DataFrame({
                    "Destination": [choix_dest, best['Destination']],
                    "Score de Risque": [info_dest['score_mensuel'], best['score_mensuel']],
                    "Type": ["Destination Risquée", "Alternative Sûre"]
                })
                
                fig_compare = px.bar(
                    chart_data, x="Score de Risque", y="Destination", color="Type", orientation='h', text_auto=True,
                    color_discrete_map={"Destination Risquée": "#e74c3c", "Alternative Sûre": "#2ecc71"}
                )
                fig_compare.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white", showlegend=False, height=200, margin={"l": 0, "r": 0, "t": 30, "b": 0})
                st.plotly_chart(fig_compare, use_container_width=True)
            else:
                st.warning("Aucune destination sûre trouvée dans votre base de données.")

else:
    st.info("👋 Bonjour ! Chargez votre fichier Excel à gauche.")
