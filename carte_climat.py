import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 🧩 LE "CERVEAU" MONDIAL (DATABASE INTÉGRÉE)
# ==============================================================================
WORLD_CLIMATE_DATA = {
    # --- AFRIQUE ---
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

    # --- ASIE ---
    'afghanistan': {'lat': 33.93, 'lon': 67.70, 'score': 80, 'cause': 'Sécheresse & Instabilité'},
    'arabie saoudite': {'lat': 23.88, 'lon': 45.07, 'score': 90, 'cause': 'Chaleur Extrême'},
    'armenie': {'lat': 40.06, 'lon': 45.03, 'score': 55, 'cause': 'Désertification'},
    'azerbaidjan': {'lat': 40.14, 'lon': 47.57, 'score': 60, 'cause': 'Baisse niveau Caspienne'},
    'bangladesh': {'lat': 23.68, 'lon': 90.35, 'score': 95, 'cause':
