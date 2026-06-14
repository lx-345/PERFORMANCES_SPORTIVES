import sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook

# Imports de tes modules de reporting Excel existants
from src.performances_sportives.reporting.backend import construire_onglets_back
from src.performances_sportives.reporting.bilan import construire_page_bilan
from src.performances_sportives.reporting.analyse import construire_page_analyse
from src.performances_sportives.reporting.charge import construire_page_charge

# URL pré-signée fournie (Directement connectée à ton fichier propre sur Onyxia)
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
    print("\n" + "="*60)
    print("🚀 PIPELINE REPORTING : REQUÊTE DIRECTE ONYXIA 🚀")
    print("="*60 + "\n")
    
    # --- PHASE 1 : REQUÊTE ET CHARGEMENT DE LA BASE EN LIGNE ---
    try:
        print("🌐 Téléchargement et lecture des données propres depuis Onyxia...")
        # Pandas télécharge et convertit directement l'URL en DataFrame
        df_export = pd.read_csv(URL_DONNEES_CLEAN)
        print(f"📊 Données récupérées avec succès ({len(df_export)} lignes détectées).")
    except Exception as e:
        print(f"❌ Erreur lors de l'accès aux données Onyxia : {e}")
        print("💡 Astuce : Vérifie si le lien pré-signé n'a pas expiré (X-Amz-Expires).")
        sys.exit(1)

    # --- PHASE 2 : GÉNÉRATION DU DASHBOARD EXCEL ---
    try:
        print("\n⏳ Construction du Dashboard Pro Excel...")
        wb = Workbook()
        max_data_row = len(df_export) + 1
        trimestres_uniques = sorted(df_export['trimestre'].dropna().unique().astype(str).tolist())
        
        # 2.1 Construction du moteur caché (Backend) avec le DataFrame distant
        len_y, len_t, len_d, len_s, len_n, max_pivot_row = construire_onglets_back(
            wb, df_export, trimestres_uniques, max_data_row
        )
        
        # 2.2 Construction des pages d'en-tête et visuelles
        construire_page_bilan(wb, max_data_row, len_y, len_s, len_n)
        construire_page_analyse(wb, max_data_row, len_y, len_t, len_d, max_pivot_row)
        construire_page_charge(wb, max_data_row, len_y, len_t, len_d)
        
        # 2.3 Nettoyage final du classeur et masquage technique
        if "Sheet" in wb.sheetnames: 
            del wb["Sheet"]
        wb["RESSOURCES"].sheet_state = 'hidden'
        wb["DATA"].sheet_state = 'hidden'
        wb["Data_Pivot"].sheet_state = 'hidden'
            
        # 2.4 Sauvegarde locale du fichier final
        dossier_reporting = Path("reporting")
        dossier_reporting.mkdir(parents=True, exist_ok=True)
        chemin_fichier = dossier_reporting / "Dashboard_Pro_Strava.xlsx"
        
        wb.save(str(chemin_fichier))
        
        print("\n" + "="*60)
        print(f"✅ DASHBOARD GÉNÉRÉ AVEC SUCCÈS ! ✅")
        print(f"Livrable disponible localement dans : {chemin_fichier}")
        print("="*60 + "\n")
        
    except PermissionError:
        print("\n❌ ERREUR : Le fichier Excel 'Dashboard_Pro_Strava.xlsx' est déjà ouvert.")
        print("Ferme-le et relance le script.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur critique lors de la génération Excel : {e}")
        sys.exit(1)

if __name__ == "__main__":
    executer_generation_dashboard()