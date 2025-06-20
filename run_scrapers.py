from scrapers.royalairmaroc.scraper import RoyalAirMarocScraper
from scrapers.cgi.scraper import CGIESourcingScraper
from scrapers.marchespublics.scraper import MarchesPublicsScraper
from scrapers.marsamaroc.scraper import MarsaMarocScraper
from scrapers.adm.scraper import AdmScraper
from scrapers.offresonline.scraper import OffresonlineScraper
import json
import os

def merge_tender_data():
    print("\nFusion des données des différentes sources...")
    consolidated_data = {}
    
    # Liste des sources et leurs chemins de fichiers
    sources = {
        'ram_esourcing': 'data/royalairmaroc/ram_esourcing_tenders.json',
        'cgi': 'data/cgi/cgi_tenders.json',
        'marchespublics': 'data/marchespublics/marches_publics_tenders.json',
        'marsamaroc': 'data/marsamaroc/marsa_maroc_tenders.json',
        'adm': 'data/adm/adm_tenders.json',
        'offresonline': 'data/offresonline/offresonline_tenders.json'
    }
    
    # Charger les données de chaque source
    for source_name, json_path in sources.items():
        consolidated_data[source_name] = []
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    tenders = json.load(f)
                    consolidated_data[source_name] = tenders
                print(f"Données chargées depuis {json_path}")
            except Exception as e:
                print(f"Erreur lors du chargement de {json_path}: {str(e)}")
    
    # Sauvegarder les données consolidées
    os.makedirs('data/consolidated', exist_ok=True)
    consolidated_path = 'data/consolidated/tenders.json'
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, ensure_ascii=False, indent=2)
    
    print(f"Données consolidées sauvegardées dans {consolidated_path}")
    print(f"Nombre total d'appels d'offres: {len(consolidated_data)}")

def main():
    print("=== Démarrage du scraping des appels d'offres ===")
    
    # Royal Air Maroc Scraping
    print("\n=== Royal Air Maroc E-Sourcing ===")
    ram_scraper = RoyalAirMarocScraper()
    ram_scraper.scrape()
    
    # CGI Scraping
    print("\n=== CGI E-Sourcing ===")
    cgi_scraper = CGIESourcingScraper()
    cgi_scraper.scrape()
    
    # Marchés Publics Scraping
    print("\n=== Marchés Publics ===")
    mp_scraper = MarchesPublicsScraper()
    mp_scraper.scrape()
    
    # Marsa Maroc Scraping
    print("\n=== Marsa Maroc ===")
    mm_scraper = MarsaMarocScraper()
    mm_scraper.scrape()
    
    # ADM Scraping
    print("\n=== ADM ===")
    adm_scraper = AdmScraper()
    adm_scraper.scrape()
    
    # Offres Online Scraping
    print("\n=== Offres Online ===")
    oo_scraper = OffresonlineScraper()
    oo_scraper.scrape()
    
    # Merge data
    merge_tender_data()
    
    print("\n=== Scraping terminé ===\n")

if __name__ == '__main__':
    main()