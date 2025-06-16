from playwright.sync_api import sync_playwright
import pandas as pd
import json
import os
from datetime import datetime

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
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Accéder à la page d'authentification
                print("Accès à la page d'authentification...")
                page.goto(self.base_url)
                page.wait_for_load_state('networkidle')
                
                # Fermer le popup
                print("Fermeture du popup...")
                try:
                    page.wait_for_selector('#modalMarsa > div > div > div.modal-footer > button', timeout=10000)
                    page.click('#modalMarsa > div > div > div.modal-footer > button')
                except Exception as e:
                    print("Pas de popup à fermer ou popup déjà fermé")
                
                # Login
                print("Tentative de connexion...")
                page.fill('#ctl0_CONTENU_PAGE_login', self.username)
                page.fill('#ctl0_CONTENU_PAGE_password', self.password)
                page.click('#ctl0_CONTENU_PAGE_authentificationButton')
                
                # Attendre que la page se charge après la connexion
                print("Attente de chargement après connexion...")
                page.wait_for_load_state('networkidle')
                page.wait_for_load_state('domcontentloaded')
                page.wait_for_timeout(10000)  # Attente de 10 secondes après la connexion
                
                # Vérifier si la connexion a réussi
                error_message = page.query_selector('.error-message')
                if error_message:
                    raise Exception(f"Échec de connexion: {error_message.inner_text()}")
                print("Connexion réussie!")
                
                # Accéder directement à la page des appels d'offre
                print("Navigation vers la liste des appels d'offres...")
                try:
                    # Naviguer directement vers l'URL des appels d'offres
                    page.goto('https://achats.marsamaroc.co.ma/?page=entreprise.EntrepriseAdvancedSearch&AllCons&searchAnnCons')
                    print("Navigation directe vers la page des appels d'offres...")
                    
                    # Attendre que la page soit complètement chargée
                    print("Attente du chargement complet de la page...")
                    page.wait_for_load_state('networkidle')
                    page.wait_for_load_state('domcontentloaded')
                    page.wait_for_timeout(10000)  # Attente de 10 secondes après la navigation
                    
                except Exception as e:
                    raise Exception(f"Erreur lors de la navigation: {str(e)}")
                
                # Extract data
                print("Extraction des données...")
                tenders = []
                
                try:
                    # Attendre que le conteneur principal soit visible
                    print("Recherche du conteneur principal...")
                    page.wait_for_selector('#tabNav', timeout=30000)
                    page.wait_for_selector('div.content', timeout=30000)
                    
                    # Trouver tous les appels d'offre
                    print("Recherche des appels d'offre...")
                    tender_items = page.query_selector_all('#tabNav div.content > div')
                    
                    if not tender_items:
                        print("Tentative avec un sélecteur alternatif...")
                        tender_items = page.query_selector_all('div.content div.row')
                    
                    if not tender_items:
                        print("Aucun appel d'offre trouvé.")
                        return []
                    
                    print(f"Nombre d'appels d'offre trouvés: {len(tender_items)}")
                    
                    for item in tender_items:
                        tender = {}
                        
                        # Extract object
                        print("Extraction de l'objet...")
                        object_elem = item.query_selector('div.p-objet, div.objet, .objet')
                        if object_elem:
                            tender['objet'] = object_elem.inner_text().strip()
                            print(f"Objet trouvé: {tender['objet'][:50]}...")
                        else:
                            print("Objet non trouvé avec le sélecteur principal, tentative avec le texte complet...")
                            tender['objet'] = item.inner_text().strip()
                            print(f"Texte complet extrait: {tender['objet'][:50]}...")
                        
                        # Extract deadline date
                        print("Extraction de la date limite...")
                        date_selectors = [
                            'span[style="display:;"]',
                            'span.date-limite',
                            '.date_limite',
                            'div.date-limite'
                        ]
                        date_elem = None
                        for selector in date_selectors:
                            date_elem = item.query_selector(selector)
                            if date_elem:
                                break
                        
                        if date_elem:
                            tender['date_limite'] = date_elem.inner_text().strip()
                            print(f"Date limite trouvée: {tender['date_limite']}")
                        else:
                            print("Date limite non trouvée dans cet élément")
                            tender['date_limite'] = 'N/A'
                        
                        if tender:
                            tenders.append(tender)
                            print("Appel d'offre ajouté à la liste")
                        
                except Exception as e:
                    print(f"Erreur détaillée lors de l'extraction: {str(e)}")
                    raise Exception(f"Erreur lors de l'extraction des appels d'offre: {str(e)}")
                
                browser.close()
                
                # Export data
                print(f"Exportation de {len(tenders)} appels d'offres...")
                self._export_data(tenders)
                
                print("Scraping terminé avec succès!")
                return tenders
                
        except Exception as e:
            print(f"\nERREUR lors du scraping: {str(e)}")
            return []
    
    def _export_data(self, tenders):
        try:
            # Export to text file
            print("Exportation vers fichier texte...")
            txt_path = f'{self.data_dir}/data.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                for tender in tenders:
                    f.write(f"Object: {tender.get('objet', 'N/A')}\n")
                    f.write(f"Date Limite: {tender.get('date_limite', 'N/A')}\n")
                    f.write('---\n')
            print(f"Données exportées vers {txt_path}")
        
            # Export to JSON
            print("Exportation vers JSON...")
            json_path = f'{self.data_dir}/marsa_maroc_tenders.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(tenders, f, ensure_ascii=False, indent=2)
            print(f"Données exportées vers {json_path}")
        
            # Export to Excel
            print("Exportation vers Excel...")
            excel_path = f'{self.data_dir}/marsa_maroc_tenders.xlsx'
            df = pd.DataFrame(tenders)
            df.to_excel(excel_path, index=False)
            print(f"Données exportées vers {excel_path}")
            
        except Exception as e:
            print(f"Erreur lors de l'exportation des données: {str(e)}")