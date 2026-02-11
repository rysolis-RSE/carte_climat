# 🌍 Cockpit de Pilotage RSE & Climat - Voyageurs du Monde

### 🚀 Vision du Projet
Ce projet est une **application de Business Intelligence & Data Science** conçue pour piloter la stratégie RSE du groupe *Voyageurs du Monde*. 

Contrairement aux tableaux de bord classiques, cet outil ne se contente pas de mesurer le passé : il utilise l'IA pour **segmenter les performances** et projeter les **risques climatiques futurs** sur le modèle économique.

---

### ⚡ Fonctionnalités Clés

#### 1. 📊 Dashboard de Performance (Decoupling)
- Analyse en temps réel du ratio **Croissance Clients vs Émissions CO2**.
- Calcul automatique du "Score de Découplage" par filiale.
- Visualisation KPI interactifs (Plotly).

#### 2. 🤖 Segmentation IA (Machine Learning)
- Utilisation de l'algorithme **K-Means** (Scikit-Learn) pour identifier 3 profils de filiales :
    - 🌟 **Leaders :** Forte croissance, faible intensité carbone.
    - ⚖️ **Stables :** Performance moyenne.
    - ⚠️ **À Risque :** Dérive carbone importante.

#### 3. 🌍 Carte des Risques Climatiques (Geospatial Intelligence)
- Cartographie interactive de **+190 destinations**.
- **Base de données climatique intégrée** : Évaluation automatique de la vulnérabilité physique des destinations (Stress hydrique, Montée des eaux, Fonte arctique).
- Analyse de l'exposition du Chiffre d'Affaires aux risques +2°C.

#### 4. 💬 Assistant Virtuel RSE
- Chatbot intelligent capable de répondre aux questions sur les données (*"Qui est le meilleur ?", "Quel est le bilan du Maroc ?"*).
- Moteur de règles (Rule-Based) avec reconnaissance d'alias.

#### 5. 🔮 Simulateur & Finance
- Projection des émissions à horizon 2030 selon hypothèses de croissance.
- Calcul du **Risque Financier** (Shadow Carbon Pricing).
- Génération automatique de **Rapports PDF** pour le Comex.

---

### 🛠️ Stack Technique

* **Langage :** Python 3.9+
* **Interface :** Streamlit
* **Data Viz :** Plotly Express / Graph_Objects
* **Machine Learning :** Scikit-Learn (KMeans)
* **Data Engineering :** Pandas (Nettoyage & Consolidation)
* **Export :** FPDF

---

### ⚙️ Installation & Lancement

1. **Cloner le projet**
   ```bash
   git clone [https://github.com/ton-pseudo/cockpit-rse.git](https://github.com/ton-pseudo/cockpit-rse.git)
   cd cockpit-rse