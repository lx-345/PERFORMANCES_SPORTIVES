import pandas as pd
import numpy as np
from pathlib import Path

# Sécurisation des chemins : on remonte à la racine du projet (3 niveaux au-dessus)
ROOT_DIR = Path(__file__).resolve().parents[3]

def nettoyer_donnees_strava(nom_fichier_entree="activites_brutes.csv", nom_fichier_sortie="activites_clean.csv"):
    """
    Lit le fichier brut, nettoie les données, crée les KPIs physiologiques
    et sauvegarde le fichier propre dans le dossier data/.
    """
    print("\n⏳ Démarrage du nettoyage des données Strava...")
    
    # 1. CIBLAGE DU DOSSIER DATA
    dossier_data = ROOT_DIR / "data"
    
    # Recherche du fichier brut (gestion du sous-dossier 'raw' vu sur ton arborescence)
    chemin_brut = dossier_data / "raw" / nom_fichier_entree
    if not chemin_brut.exists():
        chemin_brut = dossier_data / nom_fichier_entree # Fallback directement dans data/
        
    if not chemin_brut.exists():
        raise FileNotFoundError(f"❌ Le fichier brut est introuvable. Chemins testés :\n- {dossier_data / 'raw' / nom_fichier_entree}\n- {dossier_data / nom_fichier_entree}")
    
    print(f"📥 Lecture des données brutes depuis : {chemin_brut}")
    df = pd.read_csv(chemin_brut)
    
    # 2. Filtrage des courses à pied
    types_run = ['Run', 'TrailRun', 'VirtualRun']
    mots_cles = ['run', 'course', 'trail', '400', 'séance', 'entraînement']
    masque_run = (df['type'].isin(types_run)) | (df['name'].str.lower().str.contains('|'.join(mots_cles), na=False))
    masque_exclure = df['name'].str.lower().str.contains('vélo|musculation|poids|randonnée|marche', na=False)
    df_strava = df[masque_run & ~masque_exclure].copy()
    
    # 3. Conversions métriques de base
    df_strava['distance_km'] = df_strava['distance'] / 1000
    df_strava['moving_time_min'] = df_strava['moving_time'] / 60
    df_strava['average_speed_kmh'] = (df_strava['average_speed'] * 3.6).round(2)
    
    # 4. Variables temporelles
    df_temp_date = pd.to_datetime(df_strava['start_date_local'], errors='coerce')
    df_strava['jour'] = df_temp_date.dt.day_name(locale='fr_FR').str.capitalize()
    df_strava['semaine'] = df_temp_date.dt.isocalendar().week.astype(str)
    df_strava['trimestre'] = df_temp_date.dt.to_period('Q').astype(str)
    df_strava['annee'] = df_temp_date.dt.year.astype(str)
    df_strava['start_date_local'] = df_temp_date.dt.date
    df_strava = df_strava.sort_values('start_date_local')
    
    # 5. Classification des distances cibles
    conditions = [
        df_strava['distance_km'].between(4.5, 5.5),
        df_strava['distance_km'].between(9.5, 10.5),
        df_strava['distance_km'].between(20.5, 21.5),
        df_strava['distance_km'].between(41.0, 43.5)
    ]
    choices = ['5K', '10K', '21K', 'Marathon']
    df_strava['distance_cible'] = pd.Series(np.select(conditions, choices, default='Autre'), index=df_strava.index)
    
    # 6. Physiologie (VMA, Karvonen, Stress Méca)
    FC_REPOS, FC_MAX, POIDS = 45, 190, 71
    df_strava['average_heartrate'] = pd.to_numeric(df_strava.get('average_heartrate', 0), errors='coerce')
    df_strava["indice_d_effort_K"] = ((df_strava['average_heartrate'] - FC_REPOS) / (FC_MAX - FC_REPOS)).round(2)
    
    df_strava['VMA'] = np.where(df_strava["indice_d_effort_K"] > 0, 
                                (df_strava['average_speed_kmh'] / df_strava["indice_d_effort_K"]).round(2), np.nan)
    
    df_strava["Puissance_VMA"] = POIDS * df_strava["VMA"].fillna(18.0) * 0.28
    
    df_strava["average_watts"] = pd.to_numeric(df_strava.get("average_watts", 0), errors="coerce").fillna(0)
    df_strava["typologie_terrain"] = np.where(df_strava['name'].str.lower().str.contains('trail'), 'meuble', 'dure')
    df_strava["C_sol"] = np.where(df_strava["typologie_terrain"] == "dure", 1.2, 1.0)
    
    df_strava["stress_mecanique"] = (
        df_strava["moving_time_min"] * (df_strava["average_watts"] / df_strava["Puissance_VMA"].replace(0, np.nan)) ** 2 * df_strava["C_sol"]
    ).round(3)
    
    # 7. Classification Machine Learning (Intensité)
    s_cardio = np.percentile(df_strava['indice_d_effort_K'].fillna(0), [30, 80])
    s_meca = np.percentile(df_strava['stress_mecanique'].fillna(0), [30, 80])
    
    def pre_class(r):
        if r["indice_d_effort_K"] >= s_cardio[1] or r["stress_mecanique"] >= s_meca[1]: 
            return "Intense"
        elif r["indice_d_effort_K"] <= s_cardio[0] and r["stress_mecanique"] <= s_meca[0]: 
            return "Faible"
        else: 
            return "Modéré"
            
    df_strava['type_entrainement'] = df_strava.apply(pre_class, axis=1)

    # 8. NETTOYAGE FINAL ET SAUVEGARDE
    colonnes_utiles = ['name', 'start_date_local', 'annee', 'trimestre', 'distance_cible', 'distance_km', 'moving_time_min', 'VMA', 'indice_d_effort_K', 'stress_mecanique', 'type_entrainement', 'jour', 'semaine']
    df_export = df_strava[colonnes_utiles].copy()
    
    # Création explicite du fichier au même endroit
    chemin_clean = dossier_data / nom_fichier_sortie
    
    # LIGNE CRUCIALE : Force la création du dossier parent (data/) s'il n'existe pas encore
    chemin_clean.parent.mkdir(parents=True, exist_ok=True)
    
    df_export.to_csv(chemin_clean, index=False, encoding='utf-8')
    
   
    
    return df_export

if __name__ == "__main__":
    nettoyer_donnees_strava()