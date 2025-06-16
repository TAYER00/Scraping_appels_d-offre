import os
import sys
import json
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime

# Add the project root directory to Python path if not already added
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

class DataConsolidator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        # Créer un dossier 'global' pour les fichiers consolidés
        self.global_dir = os.path.join(os.path.dirname(self.output_dir), 'global')
        os.makedirs(self.global_dir, exist_ok=True)
        
    def consolidate_and_export(self, all_results: Dict[str, List[Dict[str, Any]]]):
        """Consolide et exporte les données dans différents formats."""
        # Préparer les données consolidées
        consolidated_data = []
        
        # Vérifier si nous avons des résultats à traiter
        if not all_results:
            print("Aucun résultat à consolider.")
            return
            
        for site_name, tenders in all_results.items():
            if not isinstance(tenders, list):
                print(f"Warning: Les données pour {site_name} ne sont pas une liste. Ignoré.")
                continue
                
            for tender in tenders:
                if not isinstance(tender, dict):
                    print(f"Warning: Un appel d'offres de {site_name} n'est pas un dictionnaire. Ignoré.")
                    continue
                    
                tender_data = {
                    'site': site_name,
                    'objet': tender.get('objet', 'N/A') if isinstance(tender, dict) else 'N/A',
                    'date_limite': tender.get('date_limite', 'N/A') if isinstance(tender, dict) else 'N/A'
                }
                consolidated_data.append(tender_data)
        
        # Si aucune donnée valide n'a été trouvée, arrêter ici
        if not consolidated_data:
            print("Aucune donnée valide à exporter.")
            return
        
        # Créer le timestamp pour les noms de fichiers
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        try:
            # Export dans le dossier de la session courante
            self._export_to_text(consolidated_data, timestamp, self.output_dir, 'session')
            self._export_to_json(consolidated_data, timestamp, self.output_dir, 'session')
            self._export_to_excel(consolidated_data, timestamp, self.output_dir, 'session')
            self._generate_statistics(consolidated_data, timestamp, self.output_dir)
            
            # Export dans le dossier global
            self._export_to_text(consolidated_data, timestamp, self.global_dir, 'global')
            self._export_to_json(consolidated_data, timestamp, self.global_dir, 'global')
            self._export_to_excel(consolidated_data, timestamp, self.global_dir, 'global')
            self._generate_statistics(consolidated_data, timestamp, self.global_dir)
            
            print("Export des données terminé avec succès.")
            
        except Exception as e:
            print(f"Erreur lors de l'export des données: {str(e)}")
    
    def _export_to_text(self, data: List[Dict[str, Any]], timestamp: str, output_dir: str, export_type: str):
        """Exporte les données en format texte."""
        prefix = 'global' if export_type == 'global' else 'consolidated'
        output_file = os.path.join(output_dir, f'{prefix}_tenders_{timestamp}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Appels d'offres consolidés ===\n\n")
            # Organiser par site
            sites = sorted(set(tender['site'] for tender in data))
            for site in sites:
                f.write(f"\n=== {site.upper()} ===\n\n")
                site_tenders = [t for t in data if t['site'] == site]
                for tender in site_tenders:
                    f.write(f"Objet: {tender['objet']}\n")
                    f.write(f"Date limite: {tender['date_limite']}\n")
                    f.write("---\n")
        print(f"Fichier texte créé: {output_file}")
    
    def _export_to_json(self, data: List[Dict[str, Any]], timestamp: str, output_dir: str, export_type: str):
        """Exporte les données en format JSON."""
        prefix = 'global' if export_type == 'global' else 'consolidated'
        output_file = os.path.join(output_dir, f'{prefix}_tenders_{timestamp}.json')
        
        # Organiser les données par site
        organized_data = {}
        for tender in data:
            site = tender['site']
            if site not in organized_data:
                organized_data[site] = []
            organized_data[site].append({
                'objet': tender['objet'],
                'date_limite': tender['date_limite']
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(organized_data, f, ensure_ascii=False, indent=2)
        print(f"Fichier JSON créé: {output_file}")
    
    def _export_to_excel(self, data: List[Dict[str, Any]], timestamp: str, output_dir: str, export_type: str):
        """Exporte les données en format Excel."""
        prefix = 'global' if export_type == 'global' else 'consolidated'
        output_file = os.path.join(output_dir, f'{prefix}_tenders_{timestamp}.xlsx')
        
        try:
            # Créer un writer Excel
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                # Créer un onglet pour chaque site
                sites = sorted(set(tender['site'] for tender in data))
                for site in sites:
                    site_data = [{
                        'Objet': t['objet'],
                        'Date limite': t['date_limite']
                    } for t in data if t['site'] == site]
                    
                    df = pd.DataFrame(site_data)
                    df.to_excel(writer, sheet_name=site, index=False)
                    
                    # Ajuster la largeur des colonnes
                    worksheet = writer.sheets[site]
                    worksheet.set_column('A:A', 50)  # Objet
                    worksheet.set_column('B:B', 20)  # Date limite
            print(f"Fichier Excel créé: {output_file}")
        except Exception as e:
            print(f"Erreur lors de la création du fichier Excel: {str(e)}")
    
    def _generate_statistics(self, data: List[Dict[str, Any]], timestamp: str, output_dir: str):
        """Génère des statistiques sur les appels d'offres."""
        stats = {
            'total_tenders': len(data),
            'tenders_by_site': {}
        }
        
        # Calculer les statistiques par site
        for tender in data:
            site = tender['site']
            if site not in stats['tenders_by_site']:
                stats['tenders_by_site'][site] = 0
            stats['tenders_by_site'][site] += 1
        
        # Exporter les statistiques
        output_file = os.path.join(output_dir, f'statistics_{timestamp}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Statistiques des appels d'offres ===\n\n")
            f.write(f"Nombre total d'appels d'offres: {stats['total_tenders']}\n\n")
            f.write("Répartition par site:\n")
            for site, count in sorted(stats['tenders_by_site'].items()):
                f.write(f"- {site}: {count} appels d'offres\n")
        print(f"Fichier de statistiques créé: {output_file}")