import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from fpdf import FPDF
import io

# ==============================================================================
# 1. CONFIGURATION DE LA PAGE
# ==============================================================================
st.set_page_config(
    page_title="Cockpit RSE - Voyageurs du Monde",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Cockpit de Pilotage Stratégique RSE")
st.markdown("Vue d'ensemble de la performance Carbone & Financière du Groupe.")

# ==============================================================================
# 2. FONCTIONS UTILITAIRES (PDF & CHATBOT)
# ==============================================================================

def generer_pdf(dataframe, cout_financier):
    """Génère un rapport PDF simple à télécharger"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Rapport de Pilotage RSE & Financier", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Nombre de filiales auditees : {len(dataframe)}", 0, 1)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, f"RISQUE FINANCIER (Taxe Carbone) : {cout_financier:,.0f} Euros", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    # Détails
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Detail par Filiale (Top 5)", 0, 1)
    pdf.set_font("Arial", size=10)
    
    for index, row in dataframe.head(5).iterrows():
        txt = f"- {row['Société']} : Croissance {row['Croissance_Clients']:.1f}% | CO2 {row['Evolution_CO2']:.1f}%"
        # Encodage latin-1 pour gérer les accents basiques
        pdf.cell(0, 8, txt.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
        
    return pdf.output(dest='S').encode('latin-1')

def reponse_chatbot(question, df):
    """Le Cerveau du Chatbot V2"""
    q = question.lower()
    
    # 1. Gestion des Alias (Surnoms)
    alias = {"terdav": "Terres d'Aventure", "vdm": "Voyageurs du Monde", "allibert": "Allibert Trekking"}
    for k, v in alias.items():
        if k in q: q = q.replace(k, v.lower())

    # 2. Intentions
    if "meilleur" in q or "top" in q:
        best = df.loc[df['Decouplage'].idxmax()]
        return f"🏆 Le champion est **{best['Société']}** (Score Découplage : {best['Decouplage']:.1f})."
    
    if "pire" in q or "mauvais" in q:
        worst = df.loc[df['Decouplage'].idxmin()]
        return f"⚠️ Attention à **{worst['Société']}** (Dérive Carbone : {worst['Evolution_CO2']:.1f}%)."
    
    # 3. Recherche spécifique
    for societe in df['Société']:
        if str(societe).lower() in q:
            data = df[df['Société'] == societe].iloc[0]
            return f"🔎 **{societe}** : Croissance {data['Croissance_Clients']:.1f}% | CO2 {data['Evolution_CO2']:.1f}%."

    return "🤖 Je peux analyser les performances. Demandez : 'Qui est le meilleur ?' ou 'Chiffres de Terdav'."

# ==============================================================================
# 3. CHARGEMENT DES DONNÉES (DÉMO OU UPLOAD)
# ==============================================================================
st.sidebar.header("📥 Données Financières")
uploaded_file = st.sidebar.file_uploader("Charger le Bilan Carbone (Excel)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except:
        st.error("Erreur de format de fichier.")
        st.stop()
else:
    # --- DONNÉES DE DÉMO (SI PAS DE FICHIER) ---
    data_demo = {
        'Société': ['Terres d\'Aventure', 'Allibert Trekking', 'Voyageurs du Monde', 'Comptoir des Voyages', 'Nomade Aventure', 'Bivouac', 'Original Travel', 'Kevan', 'Loire Valley'],
        'Clients_N': [34479, 26913, 39496, 29109, 14381, 1500, 3183, 850, 420],
        'Clients_N_1': [34093, 26962, 39198, 29048, 14195, 1400, 2853, 800, 400],
        'CO2_N': [48053000, 32203000, 85222000, 57221000, 28492000, 2500000, 8175000, 1200000, 500000],
        'CO2_N_1': [52996000, 31958000, 99687000, 64170000, 31698000, 2600000, 8004000, 1100000, 480000]
    }
    df = pd.DataFrame(data_demo)
    st.sidebar.info("ℹ️ Mode Démo activé")

# ==============================================================================
# 4. CALCULS DES KPIS (MOTEUR)
# ==============================================================================
try:
    # Nettoyage et Calculs
    cols = ['Clients_N', 'Clients_N_1', 'CO2_N', 'CO2_N_1']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    df['Croissance_Clients'] = ((df['Clients_N'] - df['Clients_N_1']) / df['Clients_N_1']) * 100
    df['Evolution_CO2'] = ((df['CO2_N'] - df['CO2_N_1']) / df['CO2_N_1']) * 100
    df['Intensite'] = (df['CO2_N'] / df['Clients_N']) / 1000 # Tonnes/pax
    df['Decouplage'] = df['Evolution_CO2'] - df['Croissance_Clients'] # Plus c'est bas, mieux c'est
except Exception as e:
    st.error(f"Erreur de calcul : {e}")
    st.stop()

# ==============================================================================
# 5. SIDEBAR : FINANCE & EXPORT
# ==============================================================================
st.sidebar.divider()
st.sidebar.subheader("💶 Simulateur Taxe Carbone")
prix_tonne = st.sidebar.slider("Prix Tonne CO2 (€)", 0, 200, 80, 5)
quota = st.sidebar.slider("Quota Gratuit (%)", 0, 100, 20, 5) / 100

total_co2 = df['CO2_N'].sum() / 1000
cout_total = total_co2 * (1 - quota) * prix_tonne

st.sidebar.metric("Risque Financier Annuel", f"{cout_total:,.0f} €".replace(",", " "), delta="Impact sur Marge")

if st.sidebar.button("📄 Télécharger Rapport PDF"):
    pdf_bytes = generer_pdf(df, cout_total)
    st.sidebar.download_button("📥 Cliquer pour télécharger", pdf_bytes, "Rapport_RSE.pdf", "application/pdf")

# ==============================================================================
# 6. DASHBOARD (ONGLETS)
# ==============================================================================

# KPIs GLOBAUX
c1, c2, c3, c4 = st.columns(4)
c1.metric("Filiales", len(df))
c2.metric("Total Clients", f"{df['Clients_N'].sum():,.0f}")
c3.metric("Total CO2 (t)", f"{total_co2:,.0f}")
c4.metric("Découplage Moyen", f"{df['Decouplage'].mean():.1f}", delta_color="inverse")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analyse Découplage", 
    "🤖 Segmentation IA", 
    "🎯 Matrice Stratégique", 
    "🔮 Simulateur 2030", 
    "💬 Assistant IA"
])

# --- ONGLET 1 : DÉCOUPLAGE ---
with tab1:
    st.subheader("Performance : Croissance vs Pollution")
    st.caption("L'objectif est d'avoir une barre verte (Clients) haute et une barre rouge (CO2) basse, voire négative.")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Société'], y=df['Croissance_Clients'], name='Croissance Business', marker_color='#27ae60'))
    fig.add_trace(go.Bar(x=df['Société'], y=df['Evolution_CO2'], name='Évolution CO2', marker_color='#c0392b'))
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- ONGLET 2 : IA CLUSTERING ---
with tab2:
    st.subheader("Segmentation Automatique des Filiales (K-Means)")
    st.markdown("L'IA regroupe les sociétés par profil de performance.")
    
    X = df[['Croissance_Clients', 'Evolution_CO2', 'Intensite']].fillna(0)
    if len(df) >= 3:
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X)
        
        # Mapping Intelligent (Qui est le meilleur ?)
        centers = df.groupby('Cluster')['Evolution_CO2'].mean().sort_values()
        mapping = {
            centers.index[0]: "🌟 Leaders (Modèles)",
            centers.index[1]: "⚖️ Stables (Moyenne)",
            centers.index[2]: "⚠️ À Risque (Dérive)"
        }
        df['Segment'] = df['Cluster'].map(mapping)
        
        fig_ai = px.scatter(df, x="Croissance_Clients", y="Evolution_CO2", color="Segment",
                            size="CO2_N", hover_name="Société",
                            color_discrete_map={"🌟 Leaders (Modèles)": "#2ecc71", "⚠️ À Risque (Dérive)": "#e74c3c", "⚖️ Stables (Moyenne)": "#f1c40f"},
                            title="Cartographie des Profils IA")
        st.plotly_chart(fig_ai, use_container_width=True)
    else:
        st.warning("Pas assez de données pour l'IA (min 3 filiales).")

# --- ONGLET 3 : MATRICE ---
with tab3:
    st.subheader("Matrice d'Intensité")
    fig_mat = px.scatter(df, x="Croissance_Clients", y="Evolution_CO2", size="CO2_N", color="Intensite",
                         hover_name="Société", text="Société", color_continuous_scale="RdYlGn_r",
                         title="Plus c'est vert, plus le voyage est 'propre' par passager")
    fig_mat.add_hline(y=0, line_dash="dot")
    fig_mat.add_vline(x=0, line_dash="dot")
    st.plotly_chart(fig_mat, use_container_width=True)

# --- ONGLET 4 : SIMULATEUR ---
with tab4:
    st.subheader("🔮 Projection à 2030")
    col_s1, col_s2 = st.columns(2)
    hyp_croissance = col_s1.slider("Hypothèse Croissance Clients / an (%)", 0, 10, 3) / 100
    hyp_efforts = col_s2.slider("Hypothèse Réduction CO2 / an (%)", -10, 0, -5) / 100
    
    annees = list(range(2025, 2031))
    proj_co2 = [total_co2]
    
    for _ in range(5):
        # Formule : CO2 * (1 + Croissance) * (1 + Effort)
        new_co2 = proj_co2[-1] * (1 + hyp_croissance) * (1 + hyp_efforts)
        proj_co2.append(new_co2)
        
    fig_proj = px.line(x=annees, y=proj_co2, markers=True, title="Trajectoire Émissions Groupe (Tonnes CO2)")
    fig_proj.add_hline(y=proj_co2[0]*0.7, line_dash="dot", annotation_text="Objectif -30%", line_color="green")
    st.plotly_chart(fig_proj, use_container_width=True)

# --- ONGLET 5 : CHATBOT ---
with tab5:
    st.subheader("💬 Assistant Virtuel")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Posez une question sur les données..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        reponse = reponse_chatbot(prompt, df)
        
        st.session_state.messages.append({"role": "assistant", "content": reponse})
        with st.chat_message("assistant"): st.markdown(reponse)