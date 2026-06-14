import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.performances_sportives.api_strava.extract import extract_strava_pipeline
except ImportError:
    pass

try:
    from src.performances_sportives.clean.clean import nettoyer_donnees_strava
except ImportError:
    pass

try:
    from src.performances_sportives.api_onyxia.upload import upload_clean_to_onyxia
except ImportError:
    pass

try:
    from src.performances_sportives.main import executer_generation_dashboard
except ImportError:
    pass

def run_full_pipeline():
    try:
        extract_strava_pipeline()
    except Exception:
        pass

    try:
        nettoyer_donnees_strava()
    except Exception:
        pass

    try:
        upload_clean_to_onyxia()
    except Exception:
        pass

    try:
        executer_generation_dashboard()
    except Exception:
        pass

if __name__ == "__main__":
    run_full_pipeline()