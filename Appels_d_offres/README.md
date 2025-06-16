# Module de Gestion des Appels d'Offres

Ce module permet de gérer et d'automatiser le scraping des appels d'offres depuis plusieurs sites web marocains. Il consolide les données extraites dans des formats facilement exploitables.

## Sites Supportés

- Marchés Publics (marchespublics.gov.ma)
- Marsa Maroc (marsamaroc.co.ma)
- Royal Air Maroc (royalairmaroc.com)
- Offres Online (offresonline.com)
- ADM (adm.co.ma)

## Structure du Module

```
Appels_d_offres/
├── __init__.py              # Exports des classes principales
├── scraping_manager.py      # Gestion de l'exécution des scrapers
├── data_consolidator.py     # Consolidation et export des données
├── run_scrapers.py          # Script principal d'exécution
└── consolidated_data/       # Dossier des résultats consolidés
    └── YYYY-MM-DD_HH-MM-SS/ # Dossier par session de scraping
        ├── marchespublics/  # Résultats par site
        ├── marsamaroc/
        ├── royalairmaroc/
        ├── offresonline/
        └── adm/
```

## Fonctionnalités

1. **Exécution Automatisée**
   - Exécution séquentielle de tous les scrapers
   - Gestion des erreurs pour chaque scraper
   - Possibilité d'exécuter un scraper spécifique

2. **Consolidation des Données**
   - Agrégation des résultats de tous les sites
   - Export en plusieurs formats :
     - Texte (.txt)
     - JSON (.json)
     - Excel (.xlsx)
   - Génération d'un résumé statistique

3. **Organisation des Résultats**
   - Création d'un dossier daté pour chaque session
   - Séparation claire des résultats par site
   - Formats standardisés pour faciliter l'analyse

## Utilisation

1. **Exécution Complète**
   ```bash
   python run_scrapers.py
   ```
   Cette commande exécute tous les scrapers et consolide les résultats.

2. **Structure des Résultats**
   - `appels_offres_TIMESTAMP.txt` : Format texte lisible
   - `appels_offres_TIMESTAMP.json` : Format JSON structuré
   - `appels_offres_TIMESTAMP.xlsx` : Tableau Excel formaté
   - `resume_TIMESTAMP.txt` : Résumé statistique

## Maintenance et Extension

Pour ajouter un nouveau scraper :

1. Créer le scraper dans le dossier `scrapers/`
2. Ajouter la classe du scraper dans `scraping_manager.py`
3. Le nouveau site sera automatiquement intégré dans la consolidation

## Notes

- Les captures d'écran de débogage sont conservées dans les dossiers spécifiques à chaque site
- Les erreurs sont gérées individuellement pour chaque site
- Les données sont horodatées pour un suivi précis