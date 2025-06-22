from playwright.sync_api import sync_playwright
import os
import json
import pandas as pd
import re

class OffresonlineScraper:
    def __init__(self):
        self.data_dir = os.path.join('data', 'offresonline')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                print("Navigation vers la page de connexion...")
                page.goto('https://offresonline.com/')
                
                print("Clic sur le bouton de connexion...")
                page.click('#main-nav > ul > li:nth-child(2) > a')
                
                print("Attente des champs de connexion...")
                page.wait_for_selector('#Login')
                page.wait_for_selector('#pwd')
                
                print("Remplissage des informations d'authentification...")
                page.fill('#Login', 'HYATT2')
                page.fill('#pwd', 'HYATTHALMI')
                
                print("Soumission du formulaire de connexion...")
                page.click('#buuuttt')
                
                print("Attente après connexion...")
                page.wait_for_timeout(10000)
                
                print("Navigation vers la page des appels d'offres...")
                page.goto('https://offresonline.com/Admin/alert.aspx?i=a&url=5')
                
                print("Attente du chargement du tableau des appels d'offres...")
                page.wait_for_selector('#tableao')
                
                tenders = []
                for i in range(1, 13):
                    print(f"Extraction de l'appel d'offres {i}...")
                    
                    # XPath pour chaque élément
                    objet_xpath = f"//table[@id='tableao']//tr[{i}]/td[2]"
                    date_xpath = f"//table[@id='tableao']//tr[{i}]/td[3]/b[1]"
                    
                    objet_elem = page.locator(f"xpath={objet_xpath}")
                    date_elem = page.locator(f"xpath={date_xpath}")
                    
                    if objet_elem.count() == 0:
                        print(f"Ligne {i} non trouvée, passage à la suivante.")
                        continue
                    
                    objet_text = objet_elem.text_content()
                    if not objet_text:
                        print(f"Objet vide à la ligne {i}, passage à la suivante.")
                        continue
                    
                    tender = {
                        'objet': objet_text.strip()
                    }
                    
                    if date_elem.count() > 0:
                        date_text = date_elem.text_content()
                        tender['date_limite'] = date_text.strip() if date_text else 'N/A'
                    else:
                        tender['date_limite'] = 'N/A'
                    
                    # Extraction du lien dans l'attribut onclick
                    onclick = objet_elem.get_attribute('onclick')
                    if onclick:
                        # Expression simple pour extraire l'URL entre apostrophes dans window.location='...'
                        match = re.search(r"window\.location\s*=\s*'([^']+)'", onclick)
                        if not match:
                            # Essayer aussi window.open('...')
                            match = re.search(r"window\.open\s*\(\s*'([^']+)'", onclick)
                        tender['link'] = match.group(1) if match else None
                    else:
                        tender['link'] = None
                    
                    print(f"Objet: {tender['objet'][:50]}..., Date limite: {tender['date_limite']}, Link: {tender['link']}")
                    tenders.append(tender)
                
                # Sauvegarder les résultats dans offresonline_tenders.json
                json_path = os.path.join(self.data_dir, 'offresonline_tenders.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(tenders, f, ensure_ascii=False, indent=4)
                
                print(f"Données sauvegardées dans {json_path}")
                
            finally:
                browser.close()

# Pour lancer le scraper
if __name__ == "__main__":
    scraper = OffresonlineScraper()
    scraper.scrape()
