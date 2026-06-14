import os
import s3fs
from pathlib import Path
from dotenv import load_dotenv

dossier_courant = Path.cwd()
if dossier_courant.name == "notebooks":
    ROOT_DIR = dossier_courant.parent
else:
    ROOT_DIR = dossier_courant

load_dotenv(dotenv_path=ROOT_DIR / ".env")

chemin_local = ROOT_DIR / "data" / "activites_clean.csv"
chemin_s3 = "paleo/donnees_strava/activites_clean.csv"

def upload_clean_to_onyxia():
    if not chemin_local.exists():
        return

    try:
        fs = s3fs.S3FileSystem(
            client_kwargs={'endpoint_url': f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
            key=os.getenv('AWS_ACCESS_KEY_ID'),
            secret=os.getenv('AWS_SECRET_ACCESS_KEY'),
            token=os.getenv('AWS_SESSION_TOKEN')
        )
        
        fs.put(str(chemin_local), chemin_s3)
        
    except Exception:
        pass

if __name__ == "__main__":
    upload_clean_to_onyxia()