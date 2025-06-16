from playwright.sync_api import sync_playwright
import os
import json
import pandas as pd
from datetime import datetime

class OffresonlineScraper:
    def __init__(self):
        self.data_dir = os.path.join('data', 'offresonline')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Accéder à la page de connexion
                print("Navigation vers la page de connexion...")
                page.goto('https://offresonline.com/')
                
                # Cliquer sur le bouton de connexion
                print("Clic sur le bouton de connexion...")
                page.click('#main-nav > ul > li:nth-child(2) > a')
                
                # Attendre que les champs de connexion soient visibles
                page.wait_for_selector('#Login')
                page.wait_for_selector('#pwd')
                
                # Remplir les informations d'authentification
                print("Remplissage des informations d'authentification...")
                page.fill('#Login', 'HYATT2')
                page.fill('#pwd', 'HYATTHALMI')
                
                # Cliquer sur le bouton de soumission
                print("Soumission du formulaire de connexion...")
                page.click('#buuuttt')
                
                # Attendre 10 secondes après la connexion
                page.wait_for_timeout(10000)
                
                # Prendre une capture d'écran après la connexion
                page.screenshot(path=os.path.join(self.data_dir, 'post_login.png'))
                
                # Naviguer vers la page des appels d'offres
                print("Navigation vers la page des appels d'offres...")
                page.goto('https://offresonline.com/Admin/alert.aspx?i=a&url=5')
                
                # Attendre 10 secondes après la navigation
                page.wait_for_timeout(10000)
                
                # Prendre une capture d'écran après la navigation
                page.screenshot(path=os.path.join(self.data_dir, 'post_navigation.png'))
                
                # Attendre que le tableau des appels d'offres soit visible
                print("Attente du chargement du tableau des appels d'offres...")
                page.wait_for_selector('#tableao')
                
                # Prendre une capture d'écran avant l'extraction
                page.screenshot(path=os.path.join(self.data_dir, 'page_before_extraction.png'))
                
                # Extraire les données
                print("Extraction des données...")
                tenders = []
                rows = page.query_selector_all('#tableao tr')
                
                for row in rows:
                    try:
                        objet = row.query_selector('td.classltdleftalert, td.classltdleftalertnonvueNB')
                        date_limite = row.query_selector('td.classltdcenteralertNB > b:nth-child(1)')
                        
                        tender = {
                            'objet': objet.text_content().strip() if objet else 'N/A',
                            'date_limite': date_limite.text_content().strip() if date_limite else 'N/A'
                        }
                        
                        tenders.append(tender)
                    except Exception as e:
                        print(f"Erreur lors de l'extraction d'une ligne : {str(e)}")
                        continue
                
                # Exporter les données
                if tenders:
                    # Export en format texte
                    with open(os.path.join(self.data_dir, 'data.txt'), 'w', encoding='utf-8') as f:
                        for tender in tenders:
                            f.write(f"Objet: {tender['objet']}\n")
                            f.write(f"Date limite: {tender['date_limite']}\n")
                            f.write("---\n")
                    
                    # Export en JSON
                    with open(os.path.join(self.data_dir, 'offresonline_tenders.json'), 'w', encoding='utf-8') as f:
                        json.dump(tenders, f, ensure_ascii=False, indent=2)
                    
                    # Export en Excel
                    df = pd.DataFrame(tenders)
                    df.to_excel(os.path.join(self.data_dir, 'offresonline_tenders.xlsx'), index=False)
                    
                    print(f"Extraction terminée. {len(tenders)} appels d'offres extraits.")
                else:
                    print("Aucun appel d'offres trouvé.")
                    
            except Exception as e:
                print(f"Une erreur est survenue : {str(e)}")
                # Prendre une capture d'écran en cas d'erreur
                page.screenshot(path=os.path.join(self.data_dir, 'error.png'))
                raise
            
            finally:
                browser.close()

if __name__ == '__main__':
    scraper = OffresonlineScraper()
    scraper.scrape()