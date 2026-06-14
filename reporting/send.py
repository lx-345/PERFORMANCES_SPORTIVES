import time
from pathlib import Path
from playwright.sync_api import sync_playwright

dossier_courant = Path.cwd()
if dossier_courant.name == "reporting":
    ROOT_DIR = dossier_courant.parent
else:
    ROOT_DIR = dossier_courant

def upload_dashboard_via_browser():
    chemin_local = ROOT_DIR / "reporting" / "Dashboard_Pro_Strava.xlsx"
    
    if not chemin_local.exists():
        print(f"Erreur : Le fichier est introuvable ici : {chemin_local}")
        return

    share_url = "https://cnam-my.sharepoint.com/:f:/g/personal/leo_panier_auditeur_lecnam_net/IgBoxoA5hv9oQaoIAqMi_2MGAbfItVm6UBanf1pgM1qq97w?e=mECm3q"
    
    # Dossier local qui va stocker tes cookies CNAM de manière sécurisée
    session_dir = ROOT_DIR / "reporting" / "browser_session"

    with sync_playwright() as p:
        # On lance le navigateur avec la session persistante
        # headless=False est OBLIGATOIRE la première fois pour que tu puisses te connecter
        context = p.chromium.launch_persistent_context(
            str(session_dir),
            headless=False, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()
        
        print("Ouverture de la page SharePoint...")
        page.goto(share_url)
        
        # --- LOGIQUE D'AUTHENTIFICATION UNIQUE ---
        # Si Microsoft te demande de te connecter, le script va attendre que tu fasses ta vie
        if "login.microsoftonline.com" in page.url or page.locator("text=Connexion").is_visible():
            print("\n" + "!"*60)
            print("ACTION REQUISE : Connecte-toi sur la fenêtre de navigation qui vient de s'ouvrir.")
            print("Valide ton MFA CNAM. Une fois que tu vois ton dossier SharePoint, le script continuera tout seul.")
            print("!"*60 + "\n")
            
            # Le script attend patiemment que l'input de dépôt OneDrive apparaisse à l'écran
            page.wait_for_selector("input[type='file']", timeout=300000) # 5 minutes max
        
        try:
            page.wait_for_selector("input[type='file']", timeout=15000)
            
            print(f"Dépôt du fichier {chemin_local.name}...")
            page.set_input_files("input[type='file']", str(chemin_local))
            
            # Temps de chargement pour l'upload (ajustable selon ta connexion)
            print("Téléversement en cours...")
            time.sleep(10)
            
            print("Fichier envoyé avec succès sur SharePoint via session sécurisée !")
            
        except Exception as e:
            print(f"Erreur lors du dépôt : {e}")
            
        finally:
            context.close()

if __name__ == "__main__":
    upload_dashboard_via_browser()