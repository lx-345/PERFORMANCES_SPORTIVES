import sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook

# Configuration du chemin racine du projet pour permettre l'importation
ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Importation des modules internes du projet
from src.performances_sportives.reporting.backend import construire_onglets_back
from src.performances_sportives.reporting.bilan import construire_page_bilan
from src.performances_sportives.reporting.analyse import construire_page_analyse
from src.performances_sportives.reporting.charge import construire_page_charge

URL_DONNEES_CLEAN = (
    "https://minio.lab.sspcloud.fr/paleo/donnees_strava/activites_clean.csv?"
    "X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&"
    "X-Amz-Credential=NJ6ENKOHGZLYBG846S3G%2F20260614%2Fus-east-1%2Fs3%2Faws4_request&"
    "X-Amz-Date=20260614T165521Z&X-Amz-Expires=604800&"
    "X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJOSjZFTktPSEdaTFlCRzg0NlMzRyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNzgxNDUzMjk1LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6Imxlby5wYW5pZXIuYXVkaXRldXJAbGVjbmFtLm5ldCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJleHAiOjE3ODIwNTgxMDQsImZhbWlseV9uYW1lIjoiUGFuaWVyIiwiZ2l2ZW5fbmFtZSI6IkxlbyIsImdyb3VwcyI6WyJVU0VSX09OWVhJQSJdLCJpYXQiOjE3ODE0NTMzMDMsImlzcyI6Imh0dHBzOi8vYXV0aC5sYWIuc3NwY2xvdWQuZnIvYXV0aC9yZWFsbXMvc3NwY2xvdWQiLCJqdGkiOiJvbnJ0cnQ6Mjg1ODU3NDUtNGUwZC1lYzkxLTA4YjMtMGQ3YTk2YTFhMGIyIiwibG9jYWxlIjoiZnIiLCJuYW1lIjoiTGVvIFBhbmllciIsInBvbGljeSI6InN0c29ubHkiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJwYWxlbyIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1zc3BjbG91ZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXNzcGNsb3VkIl0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZ3JvdXBzIGVtYWlsIiwic2lkIjoiVmVMQlZUbFNPSWRuSVpjQ0w3YXJkTkZuIiwic3ViIjoiZDAyYmZlM2EtNGEwYy00MmZmLWI1ODMtYTEwNGE5MjA5NzYwIiwidHlwIjoiQmVhcmVyIn0.nD1d5a977LN8SuZZ_zHOQspRj9JJBZ_27EvDvUC8NBu8LOjFhFMsc2SsMVC37lCIHM5RI3AJjhKC08WOc7vXEA&"
    "X-Amz-Signature=d5bb007a9979a5cc93e63f1768dbdade3296cf6f0d3d1c2d00ac208fcc510eb5&"
    "X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject"
)

def executer_generation_dashboard():
    try:
        df_export = pd.read_csv(URL_DONNEES_CLEAN)
    except Exception as e:
        print(f"Erreur lors de l'acces aux donnees Onyxia : {e}")
        sys.exit(1)

    try:
        wb = Workbook()
        max_data_row = len(df_export) + 1
        trimestres_uniques = sorted(df_export['trimestre'].dropna().unique().astype(str).tolist())
        
        len_y, len_t, len_d, len_s, len_n, max_pivot_row = construire_onglets_back(
            wb, df_export, trimestres_uniques, max_data_row
        )
        
        construire_page_bilan(wb, max_data_row, len_y, len_s, len_n)
        construire_page_analyse(wb, max_data_row, len_y, len_t, len_d, max_pivot_row)
        construire_page_charge(wb, max_data_row, len_y, len_t, len_d)
        
        if "Sheet" in wb.sheetnames: 
            del wb["Sheet"]
        wb["RESSOURCES"].sheet_state = 'hidden'
        wb["DATA"].sheet_state = 'hidden'
        wb["Data_Pivot"].sheet_state = 'hidden'
            
        dossier_reporting = ROOT_DIR / "reporting"
        dossier_reporting.mkdir(parents=True, exist_ok=True)
        chemin_fichier = dossier_reporting / "Dashboard_Pro_Strava.xlsx"
        
        wb.save(str(chemin_fichier))
        
    except PermissionError:
        print("Erreur : Le fichier Excel cible est actuellement ouvert par une autre application.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur critique lors de la generation Excel : {e}")
        sys.exit(1)

if __name__ == "__main__":
    executer_generation_dashboard()