from playwright.sync_api import sync_playwright
import pandas as pd
import json
import os
from datetime import datetime

class MarchesPublicsScraper:
    def __init__(self):
        self.base_url = 'https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseHome'
        self.username = 'HYATTNEGOCE'
        self.password = 'HYATTHALMI2009'
        self.data_dir = 'data/marchespublics'
        os.makedirs(self.data_dir, exist_ok=True)

    def scrape(self):
        print("Démarrage du scraping de marchespublics.gov.ma...")
        try:
            with sync_playwright() as p:
                print("Lancement du navigateur...")
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Login
                print("Tentative de connexion...")
                page.goto(self.base_url)
                page.fill('#ctl0_CONTENU_PAGE_login', self.username)
                page.fill('#ctl0_CONTENU_PAGE_password', self.password)
                page.click('#ctl0_CONTENU_PAGE_authentificationButton')
                
                # Vérifier si la connexion a réussi
                error_message = page.query_selector('.error-message')
                if error_message:
                    raise Exception(f"Échec de connexion: {error_message.inner_text()}")
                print("Connexion réussie!")
                
                # Navigate to tender list
                print("Navigation vers la liste des appels d'offres...")
                try:
                    page.wait_for_selector('#menuAnnonces > li:nth-child(3) > a', timeout=5000)
                    page.click('#menuAnnonces > li:nth-child(3) > a')
                except Exception as e:
                    raise Exception("Menu des annonces non trouvé. Vérifiez si vous êtes bien connecté.")
                
                print("Lancement de la recherche...")
                page.click('#ctl0_CONTENU_PAGE_AdvancedSearch_lancerRecherche')
                
                # Extract data
                print("Extraction des données...")
                tenders = []
                table_selector = '#tabNav > div.ongletLayer > div.content > table'
                try:
                    page.wait_for_selector(table_selector, timeout=5000)
                    rows = page.query_selector_all(f"{table_selector} tr")
                    if not rows:
                        print("Tableau des résultats non trouvé ou vide")
                        return []
                except Exception as e:
                    print(f"Erreur lors de l'extraction du tableau: {str(e)}")
                    return []
                
                print(f"Nombre de lignes trouvées: {len(rows)-1}")
                for row in rows[1:]:  # Skip header row
                    tender = {}
                    
                    # Extract object
                    object_elem = row.query_selector('[id^="ctl0_CONTENU_PAGE_resultSearch_tableauResultSearch_"][id$="_panelBlocObjet"]')
                    if object_elem:
                        tender['objet'] = object_elem.inner_text().strip()
                    
                    # Extract deadline date
                    deadline_elem = row.query_selector('#ctl0_CONTENU_PAGE_resultSearch_detailCons_ctl1_ctl0_dateHeureLimiteRemisePlis')
                    if deadline_elem:
                        tender['date_limite'] = deadline_elem.inner_text().strip()
                    else:
                        tender['date_limite'] = 'N/A'
                    
                    if tender and 'objet' in tender:
                        tenders.append(tender)
                
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
                    f.write(f"Objet: {tender.get('objet', 'N/A')}\n")
                    f.write(f"Date limite: {tender.get('date_limite', 'N/A')}\n")
                    f.write('---\n')
            print(f"Données exportées vers {txt_path}")
            
            # Export to JSON
            print("Exportation vers JSON...")
            json_path = f'{self.data_dir}/marches_publics_tenders.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(tenders, f, ensure_ascii=False, indent=2)
            print(f"Données exportées vers {json_path}")

            # Export to Excel
            print("Exportation vers Excel...")
            excel_path = f'{self.data_dir}/marches_publics_tenders.xlsx'
            df = pd.DataFrame(tenders)
            df.to_excel(excel_path, index=False)
            print(f"Données exportées vers {excel_path}")
            
        except Exception as e:
            print(f"Erreur lors de l'exportation des données: {str(e)}")