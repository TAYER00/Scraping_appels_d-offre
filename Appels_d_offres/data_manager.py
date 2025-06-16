import os
import glob
import json
from typing import Optional, Dict, Any
from datetime import datetime

class DataManager:
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.consolidated_dir = os.path.join(base_dir, 'consolidated_data')
        self.global_dir = os.path.join(self.consolidated_dir, 'global')
        
    def cleanup_old_files(self) -> None:
        """Supprime tous les fichiers de données précédemment générés."""
        try:
            # Supprimer les fichiers dans le dossier consolidated_data
            if os.path.exists(self.consolidated_dir):
                for item in os.listdir(self.consolidated_dir):
                    item_path = os.path.join(self.consolidated_dir, item)
                    if os.path.isdir(item_path):
                        for file in os.listdir(item_path):
                            file_path = os.path.join(item_path, file)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                        os.rmdir(item_path)
                    elif os.path.isfile(item_path):
                        os.remove(item_path)
                        
            # Recréer les dossiers nécessaires
            os.makedirs(self.consolidated_dir, exist_ok=True)
            os.makedirs(self.global_dir, exist_ok=True)
            
            print("Nettoyage des anciens fichiers terminé avec succès.")
            
        except Exception as e:
            print(f"Erreur lors du nettoyage des fichiers : {str(e)}")
    
    def get_latest_consolidated_data(self) -> Optional[Dict[str, Any]]:
        """Récupère les données du dernier fichier JSON consolidé."""
        try:
            # Rechercher tous les fichiers JSON dans le dossier global
            json_files = glob.glob(os.path.join(self.global_dir, 'global_tenders_*.json'))
            
            if not json_files:
                print("Aucun fichier JSON consolidé trouvé.")
                return None
            
            # Trier les fichiers par date de modification (le plus récent en premier)
            latest_file = max(json_files, key=os.path.getmtime)
            
            # Charger et retourner les données du fichier le plus récent
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Données chargées depuis : {os.path.basename(latest_file)}")
                return data
                
        except Exception as e:
            print(f"Erreur lors de la récupération des données consolidées : {str(e)}")
            return None
    
    def get_latest_file_path(self, file_type: str = 'json') -> Optional[str]:
        """Récupère le chemin du fichier le plus récent du type spécifié.
        
        Args:
            file_type (str): Type de fichier ('json', 'txt', 'xlsx')
            
        Returns:
            Optional[str]: Chemin du fichier le plus récent ou None si aucun fichier trouvé
        """
        try:
            pattern = os.path.join(self.global_dir, f'global_tenders_*.{file_type}')
            files = glob.glob(pattern)
            
            if not files:
                print(f"Aucun fichier {file_type} trouvé.")
                return None
            
            latest_file = max(files, key=os.path.getmtime)
            return latest_file
            
        except Exception as e:
            print(f"Erreur lors de la recherche du fichier {file_type} : {str(e)}")
            return None

if __name__ == '__main__':
    # Example usage
    data_manager = DataManager()
    
    # Nettoyer les anciens fichiers
    data_manager.cleanup_old_files()
    
    # Récupérer le chemin du dernier fichier JSON
    latest_json = data_manager.get_latest_file_path('json')
    if latest_json:
        print(f"Dernier fichier JSON : {latest_json}")
    
    # Charger les dernières données consolidées
    latest_data = data_manager.get_latest_consolidated_data()
    if latest_data:
        print("Données consolidées chargées avec succès.")