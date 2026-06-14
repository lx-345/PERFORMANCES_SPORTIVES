import os
import requests
from dotenv import load_dotenv
from pathlib import Path

dossier_courant = Path.cwd()
if dossier_courant.name == "notebooks":
    ROOT_DIR = dossier_courant.parent
else:
    ROOT_DIR = dossier_courant

load_dotenv(dotenv_path=ROOT_DIR / ".env")

def run_auth_flow():
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    code = input("Colle ton code ici : ")

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
        return data['refresh_token']
    else:
        return res.json()

if __name__ == "__main__":
    run_auth_flow()