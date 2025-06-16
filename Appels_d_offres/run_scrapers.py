import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from Appels_d_offres.scraping_manager import ScrapingManager
from Appels_d_offres.data_consolidator import DataConsolidator

def main():
    # Initialiser le gestionnaire de scraping
    scraping_manager = ScrapingManager()
    
    # Obtenir le dossier de sortie pour cette exécution
    output_dir = scraping_manager.current_run_dir
    
    print("=== Démarrage du scraping des appels d'offres ===\n")
    print(f"Les résultats seront sauvegardés dans: {output_dir}\n")
    
    # Afficher les sites disponibles
    available_sites = scraping_manager.get_available_sites()
    print(f"Sites disponibles: {', '.join(available_sites)}\n")
    
    try:
        # Exécuter tous les scrapers
        print("Exécution de tous les scrapers...")
        all_results = scraping_manager.run_all_scrapers()
        
        # Initialiser le consolidateur de données
        data_consolidator = DataConsolidator(output_dir)
        
        # Consolider et exporter les résultats
        print("\nConsolidation et export des résultats...")
        data_consolidator.consolidate_and_export(all_results)
        
        print("\n=== Scraping terminé avec succès ===")
        print(f"Les résultats consolidés sont disponibles dans: {output_dir}")
        
    except Exception as e:
        print(f"\nUne erreur est survenue: {str(e)}")
        print("Vérifiez les logs pour plus de détails.")

if __name__ == '__main__':
    main()