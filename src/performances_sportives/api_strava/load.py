import os
import s3fs
from pathlib import Path
from dotenv import load_dotenv

# Remonte à la racine du projet
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=ROOT_DIR / ".env")

# Cible le nouveau dossier data/raw à la racine
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

# Définition des chemins du fichier (Source et Destination)
chemin_s3 = "paleo/donnees_strava/activites_brutes.csv"
chemin_local = DATA_RAW_DIR / "activites_brutes.csv"

def download_from_onyxia():
    """Télécharge le fichier brut depuis Onyxia vers data/raw/"""
    print("☁️ Connexion au stockage Onyxia...")
    
    try:
        fs = s3fs.S3FileSystem(
            client_kwargs={'endpoint_url': f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
            key=os.getenv('AWS_ACCESS_KEY_ID'),
            secret=os.getenv('AWS_SECRET_ACCESS_KEY'),
            token=os.getenv('AWS_SESSION_TOKEN')
        )
        
        print(f"📥 Téléchargement en cours depuis : {chemin_s3}")
        
        fs.get(chemin_s3, str(chemin_local))
        
        print(f"✅ Succès ! Le fichier CSV a été enregistré dans : {chemin_local}")
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")
        print("💡 Astuce : Vérifie que ton AWS_SESSION_TOKEN dans le .env n'a pas expiré.")

if __name__ == "__main__":
    download_from_onyxia()