import os
import s3fs
from pathlib import Path
from dotenv import load_dotenv

# Remonte à la racine du projet
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=ROOT_DIR / ".env")

# Définition des chemins du fichier (Source locale et Destination S3)
chemin_local = ROOT_DIR / "data" / "activites_clean.csv"
chemin_s3 = "paleo/donnees_strava/activites_clean.csv"

def upload_clean_to_onyxia():
    """Envoie le fichier activites_clean.csv local vers Onyxia"""
    print("☁️ Connexion au stockage Onyxia...")
    
    # Sécurité : On vérifie que le fichier a bien été créé par clean.py avant d'essayer de l'envoyer
    if not chemin_local.exists():
        print(f"❌ Erreur : Le fichier local {chemin_local} n'existe pas.")
        print("💡 Astuce : Lance d'abord le nettoyage (clean.py) pour générer ce fichier.")
        return

    try:
        # Initialisation du client S3 (MinIO)
        fs = s3fs.S3FileSystem(
            client_kwargs={'endpoint_url': f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
            key=os.getenv('AWS_ACCESS_KEY_ID'),
            secret=os.getenv('AWS_SECRET_ACCESS_KEY'),
            token=os.getenv('AWS_SESSION_TOKEN')
        )
        
        print(f"📤 Envoi en cours vers S3 : {chemin_s3}...")
        
        # 'put' prend le fichier physique de ton ordinateur et l'envoie sur le bucket
        fs.put(str(chemin_local), chemin_s3)
        
        print(f"🚀 Succès ! Le fichier clean a été envoyé sur Onyxia avec succès.")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
        print("💡 Astuce : Vérifie que ton AWS_SESSION_TOKEN dans le fichier .env n'a pas expiré.")

if __name__ == "__main__":
    upload_clean_to_onyxia()