import os
import requests
import pandas as pd
import s3fs
import time
from pathlib import Path
from dotenv import load_dotenv

# Configuration de l'environnement
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

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
        
        # Si la page est vide, on a fini !
        if not data:
            break
            
        all_activities.extend(data)
        page += 1
        
        # Petite pause pour respecter les limites de l'API (Rate Limiting)
        time.sleep(0.5)

    print(f"✅ Terminé ! {len(all_activities)} activités récupérées au total.")
    return pd.DataFrame(all_activities)

def upload_to_onyxia(df):
    """Envoie le CSV sur MinIO (Onyxia)"""
    print("☁️ Envoi vers Onyxia (Zone Bronze)...")
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
        key=os.getenv('AWS_ACCESS_KEY_ID'),
        secret=os.getenv('AWS_SECRET_ACCESS_KEY'),
        token=os.getenv('AWS_SESSION_TOKEN')
    )

    target_path = "paleo/donnees_strava/activites_brutes.csv"

    with fs.open(target_path, 'w', encoding='utf-8') as f:
        df.to_csv(f, index=False)
    print(f"🚀 Succès ! Fichier complet envoyé sur S3.")

if __name__ == "__main__":
    try:
        access_token = get_new_access_token()
        df_final = fetch_all_activities(access_token)
        
        if not df_final.empty:
            upload_to_onyxia(df_final)
        else:
            print("⚠️ Aucune activité trouvée sur ton compte.")
            
    except Exception as e:
        print(f"\n🛑 Erreur lors du pipeline : {e}")