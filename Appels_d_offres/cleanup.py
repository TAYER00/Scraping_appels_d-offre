import os
import shutil
from datetime import datetime

def cleanup_old_data():
    """Nettoie les anciens fichiers de données tout en conservant le dossier le plus récent."""
    try:
        consolidated_dir = os.path.join('Appels_d_offres', 'consolidated_data')
        if not os.path.exists(consolidated_dir):
            print("Aucun dossier de données à nettoyer.")
            return

        # Lister tous les dossiers de session (format: YYYY-MM-DD_HH-MM-SS)
        session_dirs = [d for d in os.listdir(consolidated_dir) 
                       if os.path.isdir(os.path.join(consolidated_dir, d)) and d != 'global']

        if not session_dirs:
            print("Aucun dossier de session trouvé.")
            return

        # Trier les dossiers par date (le plus récent en premier)
        session_dirs.sort(reverse=True)

        # Garder le dossier le plus récent, supprimer les autres
        latest_dir = session_dirs[0]
        for old_dir in session_dirs[1:]:
            old_path = os.path.join(consolidated_dir, old_dir)
            try:
                shutil.rmtree(old_path)
                print(f"Suppression du dossier: {old_dir}")
            except Exception as e:
                print(f"Erreur lors de la suppression de {old_dir}: {str(e)}")

        print(f"Nettoyage terminé. Dossier conservé: {latest_dir}")

    except Exception as e:
        print(f"Erreur lors du nettoyage des données: {str(e)}")

if __name__ == '__main__':
    cleanup_old_data()