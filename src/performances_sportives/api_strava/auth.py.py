import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Remonte de 3 dossiers pour trouver la racine du projet
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=ROOT_DIR / ".env")

def run_auth_flow():
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    print("\n" + "="*50)
    print("🔐 ÉTAPE 1 : AUTORISATION")
    print("="*50)
    print("Clique sur ce lien (Ctrl+Clic) pour ouvrir la page Strava :")
    print(f"http://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all")

    print("\n" + "="*50)
    print("🔐 ÉTAPE 2 : RÉCUPÉRATION DU CODE")
    print("="*50)
    print("1. Clique sur 'Autoriser' sur la page web.")
    print("2. Tu vas atterrir sur une page d'erreur (c'est normal !).")
    print("3. Regarde la barre d'adresse de ton navigateur, cherche 'code=...'")
    print("4. Copie juste ce code (sans le '&') et colle-le ci-dessous :")

    code = input("\n👉 Colle ton code ici : ")

    print("\nGénération du nouveau jeton en cours...")
    res = requests.post(
        url="https://www.strava.com/oauth/token",
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )

    if res.status_code == 200:
        data = res.json()
        print("\n✅ SUCCÈS ! Voici ton VRAI Refresh Token avec accès à tes activités :")
        print("\n" + "*"*50)
        print(f"STRAVA_REFRESH_TOKEN={data['refresh_token']}")
        print("*"*50 + "\n")
        print("Ouvre ton fichier .env à la racine et remplace ton ancien token par celui-ci !")
    else:
        print(f"❌ Erreur : {res.json()}")

if __name__ == "__main__":
    run_auth_flow()