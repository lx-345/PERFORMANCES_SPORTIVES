import os
import s3fs
from pathlib import Path
from dotenv import load_dotenv

# --- 1. Gestion automatique des chemins ---
# On se repère grâce à l'emplacement de ce script
dossier_actuel = Path(__file__).parent       # src/api_strava
dossier_src = dossier_actuel.parent          # src
dossier_data = dossier_src / "data"          # src/data
chemin_env = dossier_actuel / ".env"         # src/api_strava/.env

# On s'assure que le dossier "data" existe, sinon on le crée
dossier_data.mkdir(parents=True, exist_ok=True)

# Définition des chemins du fichier (Source et Destination)
chemin_s3 = "paleo/donnees_strava/activites_brutes.csv"
chemin_local = dossier_data / "activites_brutes.csv"

# Chargement des clés S3
load_dotenv(dotenv_path=chemin_env)

def download_from_onyxia():
    print("☁️ Connexion au stockage Onyxia...")
    
    try:
        # Configuration de la connexion avec s3fs
        fs = s3fs.S3FileSystem(
            client_kwargs={'endpoint_url': f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
            key=os.getenv('AWS_ACCESS_KEY_ID'),
            secret=os.getenv('AWS_SECRET_ACCESS_KEY'),
            token=os.getenv('AWS_SESSION_TOKEN')
        )
        
        print(f"📥 Téléchargement en cours depuis : {chemin_s3}")
        
        # La fonction .get() télécharge le fichier directement
        fs.get(chemin_s3, str(chemin_local))
        
        print(f"✅ Succès ! Le fichier CSV a été enregistré dans : {chemin_local}")
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")
        print("💡 Astuce : Vérifie que ton AWS_SESSION_TOKEN dans le .env n'a pas expiré (il dure généralement 24h ou 7 jours).")

if __name__ == "__main__":
    download_from_onyxia()