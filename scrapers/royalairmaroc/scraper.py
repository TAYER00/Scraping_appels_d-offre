from playwright.sync_api import sync_playwright
import pandas as pd
import json
import os
from datetime import datetime

class RoyalAirMarocScraper:
    def __init__(self):
        self.base_url = 'https://ram-esourcing.royalairmaroc.com/web/login.html'
        self.username = 'assistantecom2@hyatt-negoce.com'
        self.password = 'HYATTHALMI200'
        self.data_dir = 'data/royalairmaroc'
        os.makedirs(self.data_dir, exist_ok=True)

    def scrape(self):
        print("Démarrage du scraping de ram-esourcing.royalairmaroc.com...")
        try:
            with sync_playwright() as p:
                print("Lancement du navigateur...")
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Accéder à la page d'authentification
                print("Accès à la page d'authentification...")
                page.goto(self.base_url)
                page.wait_for_load_state('networkidle')
                
                # Login
                print("Tentative de connexion...")
                page.fill('#username', self.username)
                page.fill('#password', self.password)
                page.click('#Entrer')
                
                # Attendre que la page se charge après la connexion
                print("Attente de chargement après connexion...")
                page.wait_for_load_state('networkidle')
                page.wait_for_load_state('domcontentloaded')
                page.wait_for_timeout(10000)  # Attente de 10 secondes après la connexion
                
                # Vérifier si la connexion a réussi
                print("Vérification de la connexion...")
                page.screenshot(path=f"{self.data_dir}/post_login.png")
                
                # Cliquer sur le lien vers la page des appels d'offres
                print("Navigation vers la liste des appels d'offres...")
                try:
                    post_login_selector = '#dijit__WidgetsInTemplateMixin_3 > div > div.frameWidgetContent > div:nth-child(1) > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > a'
                    page.wait_for_selector(post_login_selector, timeout=30000)
                    page.click(post_login_selector)
                    
                    # Attendre que la page soit complètement chargée
                    print("Attente du chargement complet de la page...")
                    page.wait_for_load_state('networkidle')
                    page.wait_for_load_state('domcontentloaded')
                    page.wait_for_timeout(10000)  # Attente de 10 secondes après la navigation
                    
                    # Capture d'écran après la navigation
                    print("Capture d'écran de la page des appels d'offres...")
                    page.screenshot(path=f"{self.data_dir}/post_navigation.png")
                except Exception as e:
                    raise Exception(f"Erreur lors de la navigation: {str(e)}")
                
                # Extract data
                print("Extraction des données...")
                tenders = []
                
                try:
                    # Attendre que le tableau soit visible
                    print("Recherche du tableau des appels d'offres...")
                    table_selector = '#chooseRfqFEBean > div > section > div.table-root > table'
                    page.wait_for_selector(table_selector, timeout=30000)
                    
                    # Prendre une capture d'écran pour vérifier la structure de la page
                    print("Capture d'écran de la page pour analyse...")
                    page.screenshot(path=f"{self.data_dir}/page_before_extraction.png")
                    
                    # Extraire les données des appels d'offres
                    print("Extraction des appels d'offres...")
                    rows = page.query_selector_all('#chooseRfqFEBean > div > section > div.table-root > table > tbody.list-tbody.async-list-tbody > tr')
                    
                    if not rows:
                        print("Aucun appel d'offre trouvé. Prise d'une capture d'écran...")
                        page.screenshot(path=f"{self.data_dir}/page_content.png")
                        raise Exception("Liste des appels d'offre non trouvée ou vide")
                    
                    print(f"Nombre d'appels d'offre trouvés: {len(rows)}")
                    
                    for row in rows:
                        tender = {}
                        
                        # Extract object
                        print("Extraction de l'objet...")
                        object_elem = row.query_selector('td.col_TITLE.tdMedium')
                        if object_elem:
                            tender['object'] = object_elem.inner_text().strip()
                            print(f"Objet trouvé: {tender['object'][:50]}...")
                        
                        # Extract deadline date
                        print("Extraction de la date limite...")
                        date_elem = row.query_selector('td.col_INTEREST_TIME_LIMIT.tdMedium')
                        if date_elem:
                            tender['date_limite'] = date_elem.inner_text().strip()
                            print(f"Date limite trouvée: {tender['date_limite']}")
                        else:
                            tender['date_limite'] = 'N/A'
                        
                        if tender:
                            tenders.append(tender)
                            print("Appel d'offre ajouté à la liste")
                        
                except Exception as e:
                    print(f"Erreur détaillée lors de l'extraction: {str(e)}")
                    page.screenshot(path=f"{self.data_dir}/error_screenshot.png")
                    raise Exception(f"Erreur lors de l'extraction des appels d'offre: {str(e)}")
                
                browser.close()
                
                if not tenders:
                    raise Exception("Aucun appel d'offres n'a été trouvé")
                
                # Export data
                print(f"Exportation de {len(tenders)} appels d'offres...")
                self._export_data(tenders)
                
                print("Scraping terminé avec succès!")
                return len(tenders)
                
        except Exception as e:
            print(f"\nERREUR lors du scraping: {str(e)}")
            raise
    
    def _export_data(self, tenders):
        try:
            # Export to text file
            print("Exportation vers fichier texte...")
            txt_path = f'{self.data_dir}/data.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                for tender in tenders:
                    f.write(f"Object: {tender.get('object', 'N/A')}\n")
                    f.write(f"Date Limite: {tender.get('date_limite', 'N/A')}\n")
                    f.write('---\n')
            print(f"Données exportées vers {txt_path}")
        
            # Export to JSON
            print("Exportation vers JSON...")
            json_path = f'{self.data_dir}/ram_esourcing_tenders.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(tenders, f, ensure_ascii=False, indent=2)
            print(f"Données exportées vers {json_path}")
        
            # Export to Excel
            print("Exportation vers Excel...")
            excel_path = f'{self.data_dir}/ram_esourcing_tenders.xlsx'
            df = pd.DataFrame(tenders)
            df.to_excel(excel_path, index=False)
            print(f"Données exportées vers {excel_path}")
            
        except Exception as e:
            print(f"Erreur lors de l'exportation des données: {str(e)}")
            raise