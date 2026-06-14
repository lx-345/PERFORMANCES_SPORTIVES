import os
import time
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Remonte à la racine du projet
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=ROOT_DIR / ".env")

def get_new_access_token():
    """Échange le refresh_token contre un access_token tout neuf"""
    print("🔄 Rafraîchissement du jeton Strava...")
    payload = {
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
        'grant_type': "refresh_token"
    }
    res = requests.post("https://www.strava.com/oauth/token", data=payload)
    res.raise_for_status()
    return res.json()['access_token']

def fetch_all_activities(token):
    """Récupère l'intégralité des activités avec pagination"""
    print("📡 Récupération de l'historique complet Strava...")
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f'Bearer {token}'}
    
    all_activities = []
    page = 1
    per_page = 200 # Maximum autorisé par Strava

    while True:
        print(f"   📥 Lecture de la page {page}...")
        params = {'per_page': per_page, 'page': page}
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        
        data = res.json()
        
        if not data:
            break
            
        all_activities.extend(data)
        page += 1
        time.sleep(0.5)

    print(f"✅ Terminé ! {len(all_activities)} activités récupérées au total.")
    return pd.DataFrame(all_activities)

def save_to_local_data(df):
    """Sauvegarde le DataFrame en local dans le dossier data/"""
    print("💾 Sauvegarde en local dans le dossier data/...")
    
    # Ciblage du dossier data à la racine du projet
    dossier_data = ROOT_DIR / "data"
    dossier_data.mkdir(parents=True, exist_ok=True)
    
    chemin_cible = dossier_data / "activites_brutes.csv"
    
    # Sauvegarde au format CSV
    df.to_csv(chemin_cible, index=False, encoding='utf-8')
    print(f"🚀 Succès ! Fichier brut enregistré sous : {chemin_cible}")

def extract_strava_pipeline():
    """Fonction principale d'extraction"""
    try:
        access_token = get_new_access_token()
        df_final = fetch_all_activities(access_token)
        
        if not df_final.empty:
            save_to_local_data(df_final)
        else:
            print("⚠️ Aucune activité trouvée sur ton compte.")
            
    except Exception as e:
        print(f"\n🛑 Erreur lors de l'extraction : {e}")

if __name__ == "__main__":
    extract_strava_pipeline()