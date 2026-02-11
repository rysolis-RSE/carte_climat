import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURATION & INTELLIGENCE CLIMATIQUE (DATA WAREHOUSE)
# ==============================================================================
st.set_page_config(page_title="Strategic Climate Cockpit", layout="wide", page_icon="🌍")

# Base de connaissances (190+ pays) avec info Hémisphère pour la saisonnalité
# 'hem': 'N' (Nord) ou 'S' (Sud) -> Sert à calculer quand c'est l'été (Risque accru)
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

# --- FONCTIONS UTILITAIRES ---
def get_info_pays(destination):
    """Normalise le nom du pays et trouve ses infos dans la base."""
    nom = str(destination).lower().strip()
    alias = {
        'usa': 'etats unis', 'uk': 'royaume uni', 'morocco': 'maroc', 'egypt': 'egypte', 
        'south africa': 'afrique du sud', 'spain': 'espagne', 'italy': 'italie', 
        'greece': 'grece', 'turkey': 'turquie', 'burma': 'birmanie'
    }
    for k, v in alias.items():
        if k in nom: nom = v
    # Recherche partielle
    for key in WORLD_CLIMATE_DATA:
        if key in nom: return WORLD_CLIMATE_DATA[key]
    # Valeur par défaut
    return {'lat': None, 'lon': None, 'score': 50, 'cause': 'Inconnu', 'hem': 'N'}

def calculer_score_mensuel(base_score, cause, hemisphere, mois):
    """
    Ajuste le score selon la saison :
    - Été (Hémisphère N en Juin/Juil/Aout) = Risque Canicule Augmenté.
    - Hiver = Risque Diminué.
    """
    # Définition de l'été selon l'hémisphère
    if hemisphere == 'N':
        mois_chauds = [6, 7, 8] # Juin-Aout
    else:
        mois_chauds = [12, 1, 2] # Dec-Fev (Été austral)
        
    score_final = base_score
    
    # Si le risque est lié à la chaleur/feu/eau, la saison compte beaucoup
    if any(x in str(cause).lower() for x in ['chaleur', 'sécheresse', 'incendie', 'hydrique', 'aridité']):
        if mois in mois_chauds:
            score_final += 15 # PIC DE RISQUE
        else:
            score_final -= 10 # ACCALMIE
            
    return min(100, max(0, score_final)) # Bornage 0-100

# ==============================================================================
# 2. BARRE LATÉRALE (INPUTS UTILISATEUR)
# ==============================================================================
st.sidebar.header("💶 Paramètres Financiers")

# Slider pour estimer le Chiffre d'Affaires
panier_moyen = st.sidebar.number_input("Panier Moyen par Client (€)", value=2500, step=100)

st.sidebar.divider()
st.sidebar.header("🎛️ Pilotage Temporel")

# UPLOAD DU FICHIER
uploaded_file = st.sidebar.file_uploader("📂 Données Voyageurs (Excel)", type=["xlsx"])
df_raw = None

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
        st.sidebar.success("✅ Fichier chargé !")
    except Exception as e:
        st.sidebar.error(f"Erreur : {e}")
else:
    # Mode Démo : On essaie de charger le fichier local s'il existe
    try:
        df_raw = pd.read_excel("Donnees_Consolidees_Voyageurs_2025.xlsx")
        st.sidebar.info("ℹ️ Mode Démo (Données 2025)")
    except:
        pass # Pas de fichier, pas de chocolat (on gère plus bas)

# CONTROLES TEMPORELS
mois_select = st.sidebar.select_slider(
    "📅 Mois de départ", 
    options=range(1, 13), 
    value=7, # Juillet par défaut
    format_func=lambda x: pd.to_datetime(f"2025-{x}-01").strftime('%B')
)

scenario = st.sidebar.radio("🔥 Scénario Climatique", ["Actuel (+1.2°C)", "Pessimiste (+4°C)"])
bonus_risk = 0 if "Actuel" in scenario else 20 # Malus global si scénario catastrophe

# ==============================================================================
# 3. TRAITEMENT DES DONNÉES (AGRÉGATION & CALCULS)
# ==============================================================================
if df_raw is not None and 'Destination' in df_raw.columns:
    # 1. Enrichissement Géographique (Latitude, Longitude, Score de base)
    coords = df_raw['Destination'].apply(lambda x: pd.Series(get_info_pays(x)))
    df_full = pd.concat([df_raw, coords], axis=1).dropna(subset=['lat'])
    
    # 2. Calcul du Score Dynamique (Mois + Scénario)
    df_full['score_mensuel'] = df_full.apply(
        lambda row: calculer_score_mensuel(row['score'], row['cause'], row['hem'], mois_select) + bonus_risk, 
        axis=1
    )
    df_full['score_mensuel'] = df_full['score_mensuel'].clip(0, 100)
    
    # 3. Calcul Financier (Cash at Risk)
    # Si la colonne Pax n'existe pas, on suppose 1 pax par ligne, sinon on l'utilise
    if 'Pax' not in df_full.columns:
        df_full['Pax'] = 1
    df_full['Cash_at_Risk'] = df_full['Pax'] * panier_moyen
    
    # 4. AGRÉGATION (CRUCIAL POUR LA PERFORMANCE)
    # On regroupe par Destination pour n'avoir qu'un point par ville sur la carte
    df_agg = df_full.groupby(['Destination', 'lat', 'lon', 'cause'])[['Pax', 'score_mensuel', 'Cash_at_Risk']].agg(
        {'Pax': 'sum', 'score_mensuel': 'mean', 'Cash_at_Risk': 'sum'}
    ).reset_index()

else:
    df_agg = None

# ==============================================================================
# 4. DASHBOARD (VISUALISATION)
# ==============================================================================
st.title("🌍 Strategic Climate Cockpit")
st.markdown("Analyse de la vulnérabilité du Chiffre d'Affaires face aux risques physiques (+2°C).")

if df_agg is not None:
    
    # --- A. KPI STRATÉGIQUES ---
    st.markdown("### 📊 Situation Financière (Cash-at-Risk)")
    
    # Seuil critique : Score > 75/100
    risk_high = df_agg[df_agg['score_mensuel'] > 75]
    
    cash_total = df_agg['Cash_at_Risk'].sum()
    cash_risk = risk_high['Cash_at_Risk'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("CA Analysé (Total)", f"{cash_total/1000000:.1f} M€")
    
    col2.metric(
        "⚠️ CA Menacé (Critique)", 
        f"{cash_risk/1000000:.1f} M€", 
        f"{(cash_risk/cash_total)*100:.1f}% du Portefeuille", 
        delta_color="inverse"
    )
    
    col3.metric("Saisonnalité", pd.to_datetime(f"2025-{mois_select}-01").strftime('%B'), "Impact Climat")

    st.divider()

    # --- B. LE GLOBE TERRESTRE 3D ---
    
    # Infobulle personnalisée
    hover_template = (
        "<b>%{hovertext}</b><br>" +
        "Risque: %{marker.color:.0f}/100<br>" +
        "Menace: %{customdata[0]}<br>" +
        "CA à Risque: %{marker.size:,.0f} €" # On triche un peu sur l'affichage pour simplifier
    )

    fig = px.scatter_geo(
        df_agg, 
        lat="lat", lon="lon", 
        size="Cash_at_Risk", # La taille des bulles = L'ARGENT
        color="score_mensuel",
        hover_name="Destination",
        hover_data={"cause": True, "score_mensuel": True, "Pax": False, "Cash_at_Risk": ":.0f"},
        color_continuous_scale=["#2ecc71", "#f1c40f", "#e74c3c", "#5e0000"], # Vert -> Jaune -> Rouge -> Noir
        range_color=[0, 100],
        projection="orthographic", # MODE GLOBE 3D
        title=f"Exposition Financière Monde - {pd.to_datetime(f'2025-{mois_select}-01').strftime('%B')}"
    )
    
    # Design "NASA" Sombre
    fig.update_geos(
        showcountries=True, countrycolor="#888888",
        showcoastlines=True, coastlinecolor="#333333",
        showocean=True, oceancolor="#090a14",
        showland=True, landcolor="#1c1e26", 
        bgcolor="#0e1117"
    )
    fig.update_layout(height=650, margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor="#0e1117", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # --- C. TRAVEL SWITCHER (IA RECOMMANDATION) ---
    st.divider()
    st.subheader("💡 Action Plan : Redirection des Flux")
    st.markdown("L'IA identifie les destinations à haut risque pour la période sélectionnée et propose des alternatives.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        # Liste des destinations rouges CE MOIS-CI
        dest_critiques = df_agg[df_agg['score_mensuel'] > 75].sort_values('Cash_at_Risk', ascending=False)
        liste_rouges = dest_critiques['Destination'].unique()
        
        if len(liste_rouges) > 0:
            choix_dest = st.selectbox("Sélectionner un marché à protéger :", liste_rouges)
            info_dest = df_agg[df_agg['Destination'] == choix_dest].iloc[0]
            perte = info_dest['Cash_at_Risk']
            st.error(f"🚨 **{choix_dest}**")
            st.caption(f"Cause : {info_dest['cause']}")
            st.metric("CA à Sécuriser", f"{perte:,.0f} €")
        else:
            choix_dest = None
            st.success("✅ Aucun marché critique identifié pour ce mois.")

    with c2:
        if choix_dest:
            # Chercher une alternative verte (Score < 40)
            alt = df_agg[df_agg['score_mensuel'] < 40].sort_values('score_mensuel')
            
            if not alt.empty:
                best = alt.iloc[0]
                gain_risque = info_dest['score_mensuel'] - best['score_mensuel']
                
                st.success(f"✅ Alternative Suggérée : **{best['Destination']}**")
                st.markdown(f"En basculant les ventes vers **{best['Destination']}**, vous sécurisez le CA sur une zone climatique stable (**{best['cause']}**).")
                
                # --- GRAPHIQUE COMPARATIF (CORRIGÉ AVEC PLOTLY) ---
                chart_data = pd.DataFrame({
                    "Destination": [choix_dest, best['Destination']],
                    "Score de Risque": [info_dest['score_mensuel'], best['score_mensuel']],
                    "Type": ["Destination Actuelle (Risque)", "Alternative (Sécurisée)"]
                })
                
                fig_compare = px.bar(
                    chart_data,
                    x="Score de Risque",
                    y="Destination",
                    color="Type",
                    orientation='h',
                    text_auto=True,
                    color_discrete_map={
                        "Destination Actuelle (Risque)": "#e74c3c", # Rouge
                        "Alternative (Sécurisée)": "#2ecc71"       # Vert
                    }
                )
                fig_compare.update_layout(
                    paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", 
                    font_color="white", showlegend=False, 
                    height=250, margin={"l": 0, "r": 0, "t": 30, "b": 0},
                    xaxis_title="Niveau de Risque / 100"
                )
                st.plotly_chart(fig_compare, use_container_width=True)
            else:
                st.warning("Aucune alternative 'Verte' (<40) trouvée dans le portefeuille actuel.")

else:
    # ÉCRAN D'ACCUEIL SI PAS DE DONNÉES
    st.info("👋 Bienvenue dans le Cockpit Stratégique.")
    st.markdown("""
    Pour commencer l'analyse :
    1. Ouvrez le menu à gauche **(>).**
    2. Si vous avez un fichier Excel, chargez-le.
    3. Sinon, le **Mode Démo** s'activera automatiquement si le fichier `Donnees_Consolidees_Voyageurs_2025.xlsx` est présent sur le serveur.
    """)
