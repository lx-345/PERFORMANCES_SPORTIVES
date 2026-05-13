import subprocess
import sys
from pathlib import Path

def run_script(script_path):
    """Exécute un script Python en utilisant l'environnement uv."""
    print(f"\n{'='*55}")
    print(f"▶️ DÉMARRAGE DU MODULE : {script_path.name}")
    print(f"{'='*55}")
    
    try:
        # Lancement de la commande 'uv run chemin/vers/le/script.py'
        subprocess.run(["uv", "run", str(script_path)], check=True)
        print(f"\n✅ MODULE {script_path.name} TERMINÉ AVEC SUCCÈS.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERREUR FATALE dans {script_path.name}.")
        print("🛑 Arrêt immédiat du pipeline pour éviter de corrompre les données.")
        sys.exit(1) # Arrête le programme principal si un sous-script plante

def main():
    print("🚀 --- LANCEMENT DU PIPELINE DE DONNÉES STRAVA --- 🚀")
    
    # 1. Définition des chemins relatifs (robuste peu importe l'ordinateur)
    racine = Path(__file__).parent
    dossier_api = racine / "src" / "api_strava"
    
    # On cible précisément les deux scripts dans l'ordre logique
    script_1_extraction = dossier_api / "strava_to_onyxia.py"
    script_2_importation = dossier_api / "onyxia_to_main.py"
    
    # 2. Vérification que les fichiers existent bien avant de lancer
    if not script_1_extraction.exists() or not script_2_importation.exists():
        print("❌ Erreur : Un ou plusieurs scripts sont introuvables dans src/api_strava/")
        return

    # 3. Exécution séquentielle
    # Étape 1 : Strava -> Cloud (Onyxia)
    run_script(script_1_extraction)
    
    # Étape 2 : Cloud (Onyxia) -> Ordinateur local (Dossier data)
    run_script(script_2_importation)
    
    print("\n🎉 TOUTES LES OPÉRATIONS SONT TERMINÉES ! 🎉")
    print("📁 Le fichier CSV est prêt dans le dossier 'src/data/'.")

if __name__ == "__main__":
    main()