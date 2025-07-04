from playwright.sync_api import sync_playwright
import pandas as pd
import json
import os
from datetime import datetime
import re

class MarsaMarocScraper:
    def __init__(self):
        self.base_url = 'https://achats.marsamaroc.co.ma/?page=entreprise.EntrepriseHome&goto=%2F%3Fpage%3Dentreprise.EntrepriseAccueilAuthentifie'
        self.username = 'HYATTNEGOCESERVICE'
        self.password = 'mctp42fBV+'
        self.data_dir = 'data/marsamaroc'
        os.makedirs(self.data_dir, exist_ok=True)

    def scrape(self):
        print("Démarrage du scraping de marsamaroc.co.ma...")
        try:
            with sync_playwright() as p:
                print("Lancement du navigateur...")
                browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'])
                page = browser.new_page()
                
                # Accéder à la page d'authentification
                print("Accès à la page d'authentification...")
                page.goto(self.base_url, timeout=60000)
                page.wait_for_load_state('networkidle', timeout=60000)
                
                # Fermer le popup s'il existe
                print("Vérification du popup...")
                try:
                    close_button = page.wait_for_selector('#modalMarsa > div > div > div.modal-footer > button', timeout=60000)
                    if close_button:
                        close_button.click()
                        print("Popup fermé")
                except Exception as e:
                    print("Pas de popup à fermer")
                
                # Login
                print("Tentative de connexion...")
                page.fill('#ctl0_CONTENU_PAGE_login', self.username)
                page.fill('#ctl0_CONTENU_PAGE_password', self.password)
                page.click('#ctl0_CONTENU_PAGE_authentificationButton')
                page.wait_for_load_state('networkidle', timeout=60000)
                
                # Vérifier la connexion
                print("Vérification de la connexion...")
                try:
                    menu = page.wait_for_selector('#collapseOne2', timeout=60000)
                    if menu:
                        print("Connexion réussie")
                        page.screenshot(path=os.path.join(self.data_dir, 'login_success.png'))
                except Exception as e:
                    print("Échec de la connexion")
                    raise Exception("Impossible de se connecter")
                
                # Accéder directement à la page des appels d'offres
                print("Navigation vers la page des appels d'offres...")
                page.screenshot(path=os.path.join(self.data_dir, 'before_navigation.png'))
                page.goto('https://achats.marsamaroc.co.ma/?page=entreprise.EntrepriseAdvancedSearch&AllCons&searchAnnCons', timeout=60000)
                page.wait_for_load_state('networkidle', timeout=60000)
                page.screenshot(path=os.path.join(self.data_dir, 'tenders_page.png'))
                
                # Vérifier la présence du conteneur principal
                print("Vérification du conteneur principal...")
                try:
                    main_container = page.wait_for_selector('#tabNav > div.p-2 > div.content')
                    if not main_container:
                        raise Exception("Conteneur principal non trouvé")
                except Exception as e:
                    print("Conteneur principal non trouvé")
                    raise e
                
                # Extraire les appels d'offres
                print("Extraction des appels d'offres...")
                tenders = []
                
                # Boucler sur les indices de 2 à 10 pour extraire les appels d'offres
                for index in range(2, 11):
                    try:
                        print(f"Extraction de l'appel d'offres {index}...")
                        
                        # Construire le sélecteur pour l'élément actuel
                        selector = f"#tabNav > div.p-2 > div.content > div:nth-child({index})"
                        tender_elem = page.query_selector(selector)
                        
                        if not tender_elem:
                            print(f"Élément {index} non trouvé, passage au suivant")
                            continue
                        
                        tender = {}
                        
                        # Extraire l'objet
                        print(f"Extraction de l'objet pour l'élément {index}...")
                        objet_elem = tender_elem.query_selector('div.p-objet')
                        if objet_elem:
                            tender['objet'] = objet_elem.inner_text().strip()
                            print(f"Objet trouvé: {tender['objet'][:50]}...")
                        else:
                            print(f"Pas d'objet trouvé pour l'élément {index}")
                            continue
                        
                        # Extraire la date limite
                        print(f"Extraction de la date limite pour l'élément {index}...")
                        date_elem = tender_elem.query_selector('span[style="display:;"]')
                        if date_elem:
                            tender['date_limite'] = date_elem.inner_text().strip()
                            print(f"Date limite trouvée: {tender['date_limite']}")
                        else:
                            tender['date_limite'] = 'N/A'
                        
                        # Extraire le lien
                        print(f"Extraction du lien pour l'élément {index}...")
                        link_selector = f"#tabNav > div.p-2 > div.content > div:nth-child({index})"
                        link_elem = page.query_selector(link_selector)
                        link = 'N/A'
                        if link_elem:
                            onclick = link_elem.get_attribute('onclick')
                            if onclick:
                                match = re.search(r"location\.href=['\"](.*?)['\"]", onclick)
                                if match:
                                    link = match.group(1)
                        
                        tender['link'] = link
                        print(f"Lien trouvé: {link}")
                        
                        if tender and 'objet' in tender:
                            tenders.append(tender)
                            print(f"Appel d'offres {index} ajouté avec succès")
                    
                    except Exception as e:
                        print(f"Erreur lors de l'extraction de l'élément {index}: {str(e)}")
                        continue
                
                print(f"Extraction terminée. {len(tenders)} appels d'offres extraits.")

                # Exporter les données
                if tenders:
                    self._export_data(tenders)
                    print("Export des données terminé avec succès.")
                    return tenders  # Retourner les données extraites
                
        except Exception as e:
            print(f"Erreur lors du scraping: {str(e)}")
            raise e

    def _export_data(self, tenders):
        try:
            # Export to JSON
            print("Exportation vers JSON...")
            json_path = os.path.join(self.data_dir, 'marsa_maroc_tenders.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(tenders, f, ensure_ascii=False, indent=2)
            print(f"Données exportées vers {json_path}")
            
            # Export to Excel
            print("Exportation vers Excel...")
            excel_path = os.path.join(self.data_dir, 'marsa_maroc_tenders.xlsx')
            df = pd.DataFrame(tenders)
            df.to_excel(excel_path, index=False)
            print(f"Données exportées vers {excel_path}")
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'export des données: {str(e)}")
            return False

if __name__ == '__main__':
    scraper = MarsaMarocScraper()
    scraper.scrape()