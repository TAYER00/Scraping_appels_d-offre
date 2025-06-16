import os
from datetime import datetime
from scraping_manager import ScrapingManager
from data_consolidator import DataConsolidator
from data_manager import DataManager
from cleanup import cleanup_old_data

def main():
    # Nettoyer les anciens fichiers de données
    print("\n=== Nettoyage des anciens fichiers ===")
    cleanup_old_data()
    
    # Initialiser le gestionnaire de données
    data_manager = DataManager()
    
    # Créer le dossier de sortie pour cette session
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join('Appels_d_offres', 'consolidated_data', timestamp)
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialiser le gestionnaire de scraping et le consolidateur de données
    scraping_manager = ScrapingManager()
    data_consolidator = DataConsolidator(output_dir)
    
    print("\n=== Démarrage du scraping ===")
    # Exécuter tous les scrapers disponibles
    results = scraping_manager.run_all_scrapers()
    
    print("\n=== Consolidation des données ===")
    # Consolider et exporter les résultats
    data_consolidator.consolidate_and_export(results)
    
    print("\n=== Scraping terminé avec succès ===")
    print(f"Les résultats consolidés sont disponibles dans: {output_dir}")
    
    # Afficher le chemin du dernier fichier JSON pour faciliter l'accès
    latest_json = data_manager.get_latest_file_path('json')
    if latest_json:
        print(f"\nDernier fichier JSON consolidé: {latest_json}")

if __name__ == '__main__':
    main()