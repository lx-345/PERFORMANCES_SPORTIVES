import os
import requests
import pandas as pd
import s3fs
from pathlib import Path
from dotenv import load_dotenv

# Trouver le .env dans le même dossier que ce script
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
    
    # Debug pour vérifier que les clés sont lues (tu pourras supprimer ces lignes après)
    print(f"DEBUG: Client ID utilisé -> {payload['client_id']}")

    res = requests.post("https://www.strava.com/oauth/token", data=payload)
    
    if res.status_code != 200:
        print(f"❌ Erreur Strava {res.status_code}: {res.json()}")
        res.raise_for_status()
        
    return res.json()['access_token']

def fetch_activities(token):
    """Récupère les activités sportives"""
    print("📡 Récupération des données Strava...")
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f'Bearer {token}'}
    params = {'per_page': 200}
    
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return pd.DataFrame(res.json())

def upload_to_onyxia(df):
    """Envoie le CSV sur MinIO"""
    print("☁️ Envoi vers Onyxia...")
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
        key=os.getenv('AWS_ACCESS_KEY_ID'),
        secret=os.getenv('AWS_SECRET_ACCESS_KEY'),
        token=os.getenv('AWS_SESSION_TOKEN')
    )

    target_path = "paleo/donnees_strava/activites_brutes.csv"

    with fs.open(target_path, 'w', encoding='utf-8') as f:
        df.to_csv(f, index=False)
    print(f"✅ Succès ! Données envoyées sur : {target_path}")

if __name__ == "__main__":
    try:
        access_token = get_new_access_token()
        data = fetch_activities(access_token)
        if not data.empty:
            upload_to_onyxia(data)
        else:
            print("⚠️ Aucune activité trouvée.")
    except Exception as e:
        print(f"\n🛑 Erreur : {e}")