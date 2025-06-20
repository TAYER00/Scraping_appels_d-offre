import os
import json
from datetime import datetime
from django.db.models import Count
from .models import Tender

class TenderService:
    @staticmethod
    def get_latest_consolidated_data():
        file_path = os.path.join('data', 'consolidated', 'tenders.json')
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def import_from_json():
        data = TenderService.get_latest_consolidated_data()
        if not data:
            return

        # Supprimer les anciennes données
        Tender.objects.all().delete()

        # Importer les nouvelles données
        for site, tenders in data.items():
            for tender in tenders:
                date_limite = tender.get('date_limite', None)
                if date_limite and date_limite != 'N/A':
                    try:
                        # Convertir la date du format "Mar 08 Juil 2025" en datetime
                        date_limite = datetime.strptime(date_limite, '%a %d %b %Y')
                    except ValueError:
                        date_limite = None
                else:
                    date_limite = None

                Tender.objects.create(
                    site=site,
                    objet=tender.get('objet', ''),
                    date_limite=date_limite,
                    link=tender.get('link', 'N/A')
                )

    @staticmethod
    def get_statistics():
        total_tenders = Tender.objects.count()
        tenders_by_site = list(Tender.objects.values('site').annotate(count=Count('id')))
        
        # Statistiques par site
        site_stats = {
            'keys': [stat['site'] for stat in tenders_by_site],
            'values': [stat['count'] for stat in tenders_by_site]
        }

        # Statistiques par mois
        tenders_by_date = Tender.objects.exclude(date_limite__isnull=True)\
            .values('date_limite__month', 'date_limite__year')\
            .annotate(count=Count('id'))\
            .order_by('date_limite__year', 'date_limite__month')

        month_names = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                      'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

        date_stats = {
            'keys': [],
            'values': []
        }

        for stat in tenders_by_date:
            month_name = month_names[stat['date_limite__month'] - 1]
            date_key = f"{month_name} {stat['date_limite__year']}"
            date_stats['keys'].append(date_key)
            date_stats['values'].append(stat['count'])

        return {
            'total_tenders': total_tenders,
            'tenders_by_site': site_stats,
            'tenders_by_date': date_stats
        }