import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add the project root directory to Python path if not already added
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from scrapers.marchespublics.scraper import MarchesPublicsScraper
from scrapers.marsamaroc.scraper import MarsaMarocScraper
from scrapers.royalairmaroc.scraper import RoyalAirMarocScraper
from scrapers.offresonline.scraper import OffresonlineScraper
from scrapers.adm.scraper import AdmScraper

class ScrapingManager:
    def __init__(self):
        self.scrapers = {
            'marchespublics': MarchesPublicsScraper,
            'marsamaroc': MarsaMarocScraper,
            'royalairmaroc': RoyalAirMarocScraper,
            'offresonline': OffresonlineScraper,
            'adm': AdmScraper
        }
        
        # Créer le dossier de sortie consolidé
        self.consolidated_output_dir = os.path.join('Appels_d_offres', 'consolidated_data')
        os.makedirs(self.consolidated_output_dir, exist_ok=True)
        
        # Créer un sous-dossier avec la date pour les résultats
        self.current_run_dir = os.path.join(
            self.consolidated_output_dir,
            datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        )
        os.makedirs(self.current_run_dir, exist_ok=True)
    
    def run_all_scrapers(self) -> Dict[str, List[Dict[str, Any]]]:
        """Exécute tous les scrapers et retourne leurs résultats."""
        all_results = {}
        
        for site_name, scraper_class in self.scrapers.items():
            try:
                print(f"\nDémarrage du scraping pour {site_name}...")
                scraper = scraper_class()
                
                # Créer un dossier spécifique pour ce site dans le dossier de la session actuelle
                site_output_dir = os.path.join(self.current_run_dir, site_name)
                os.makedirs(site_output_dir, exist_ok=True)
                
                # Exécuter le scraper et s'assurer que les résultats sont une liste
                results = scraper.scrape()
                if results is None:
                    results = []
                elif not isinstance(results, list):
                    results = [results] if results else []
                
                # Stocker les résultats
                all_results[site_name] = results
                
                print(f"Scraping de {site_name} terminé avec succès.")
                
            except Exception as e:
                print(f"Erreur lors du scraping de {site_name}: {str(e)}")
                all_results[site_name] = []
        
        return all_results
    
    def get_available_sites(self) -> List[str]:
        """Retourne la liste des sites disponibles pour le scraping."""
        return list(self.scrapers.keys())
    
    def run_specific_scraper(self, site_name: str) -> List[Dict[str, Any]]:
        """Exécute un scraper spécifique et retourne ses résultats."""
        if site_name not in self.scrapers:
            raise ValueError(f"Site non supporté: {site_name}")
        
        try:
            print(f"\nDémarrage du scraping pour {site_name}...")
            scraper = self.scrapers[site_name]()
            
            # Créer un dossier spécifique pour ce site
            site_output_dir = os.path.join(self.current_run_dir, site_name)
            os.makedirs(site_output_dir, exist_ok=True)
            
            # Exécuter le scraper et s'assurer que les résultats sont une liste
            results = scraper.scrape()
            if results is None:
                results = []
            elif not isinstance(results, list):
                results = [results] if results else []
            
            print(f"Scraping de {site_name} terminé avec succès.")
            return results
            
        except Exception as e:
            print(f"Erreur lors du scraping de {site_name}: {str(e)}")
            return []