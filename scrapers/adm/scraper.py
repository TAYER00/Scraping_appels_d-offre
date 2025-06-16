from playwright.sync_api import sync_playwright
import os
import json
import pandas as pd
from datetime import datetime

class AdmScraper:
    def __init__(self):
        self.data_dir = os.path.join('data', 'adm')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Accéder à la page de connexion
                print("Navigation vers la page de connexion...")
                page.goto('https://achats.adm.co.ma/?page=entreprise.EntrepriseHome&goto=')
                
                # Fermer le popup modal
                print("Fermeture du popup...")
                page.wait_for_selector('#modalADM > div > div > div.modal-footer > button')
                page.click('#modalADM > div > div > div.modal-footer > button')
                
                # Attendre que les champs de connexion soient visibles
                page.wait_for_selector('#ctl0_CONTENU_PAGE_login')
                page.wait_for_selector('#ctl0_CONTENU_PAGE_password')
                
                # Remplir les informations d'authentification
                print("Remplissage des informations d'authentification...")
                page.fill('#ctl0_CONTENU_PAGE_login', 'HYATTNEGOCESERVICE')
                page.fill('#ctl0_CONTENU_PAGE_password', 'HYATT159/*')
                
                # Prendre une capture d'écran avant la connexion
                page.screenshot(path=os.path.join(self.data_dir, 'before_login.png'))
                
                # Cliquer sur le bouton de connexion
                print("Soumission du formulaire de connexion...")
                page.click('#ctl0_CONTENU_PAGE_authentificationButton')
                
                # Attendre 10 secondes après la connexion
                page.wait_for_timeout(10000)
                
                # Prendre une capture d'écran après la connexion
                page.screenshot(path=os.path.join(self.data_dir, 'post_login.png'))
                
                # Naviguer directement vers la page des appels d'offres
                print("Navigation vers la page des appels d'offres...")
                page.goto('https://achats.adm.co.ma/?page=entreprise.EntrepriseAdvancedSearch&AllCons&searchAnnCons')
                
                # Attendre 10 secondes après la navigation
                page.wait_for_timeout(10000)
                
                # Prendre une capture d'écran après la navigation
                page.screenshot(path=os.path.join(self.data_dir, 'post_navigation.png'))
                
                # Attendre que le conteneur des appels d'offres soit visible
                print("Attente du chargement du conteneur des appels d'offres...")
                page.wait_for_selector('#tabNav > div.p-2 > div.content')
                
                # Prendre une capture d'écran avant l'extraction
                page.screenshot(path=os.path.join(self.data_dir, 'page_before_extraction.png'))
                
                # Extraire les données
                print("Extraction des données...")
                tenders = []
                tender_items = page.query_selector_all('div.contentColumn')
                
                for item in tender_items:
                    try:
                        objet = item.query_selector('div.info.p-card div.p-objet')
                        date_limite = item.query_selector('div.leftColumn div.limita span')
                        
                        tender = {
                            'objet': objet.text_content().strip() if objet else 'N/A',
                            'date_limite': date_limite.text_content().strip() if date_limite else 'N/A'
                        }
                        
                        tenders.append(tender)
                    except Exception as e:
                        print(f"Erreur lors de l'extraction d'un appel d'offres : {str(e)}")
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
                    with open(os.path.join(self.data_dir, 'adm_tenders.json'), 'w', encoding='utf-8') as f:
                        json.dump(tenders, f, ensure_ascii=False, indent=2)
                    
                    # Export en Excel
                    df = pd.DataFrame(tenders)
                    df.to_excel(os.path.join(self.data_dir, 'adm_tenders.xlsx'), index=False)
                    
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
    scraper = AdmScraper()
    scraper.scrape()