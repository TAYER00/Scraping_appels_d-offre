from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
import os
import json
from datetime import datetime

class TenderViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            # Get the consolidated data directory
            consolidated_dir = os.path.join('Appels_d_offres', 'consolidated_data', 'global')
            
            # Find the latest JSON file
            json_files = [f for f in os.listdir(consolidated_dir) if f.endswith('.json')]
            if not json_files:
                return Response({'error': 'No data files found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Sort files by timestamp in filename
            latest_file = sorted(json_files, key=lambda x: datetime.strptime(
                x.split('_')[-1].replace('.json', ''), '%Y-%m-%d_%H-%M-%S'
            ))[-1]
            
            # Read the latest file
            with open(os.path.join(consolidated_dir, latest_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Transform data for frontend consumption
            transformed_data = []
            for site, tenders in data.items():
                for tender in tenders:
                    transformed_data.append({
                        'site': site,
                        'objet': tender.get('objet', 'N/A'),
                        'date_limite': tender.get('date_limite', 'N/A'),
                        'id': f"{site}_{len(transformed_data)}"
                    })
            
            return Response({
                'tenders': transformed_data,
                'last_updated': latest_file.split('_')[-1].replace('.json', '')
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch tender data: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        try:
            # Get the latest data
            response = self.list(request)
            if response.status_code != 200:
                return response
            
            tenders = response.data['tenders']
            
            # Calculate statistics
            stats = {
                'total_tenders': len(tenders),
                'tenders_by_site': {},
                'tenders_by_date': {}
            }
            
            for tender in tenders:
                # Count by site
                site = tender['site']
                stats['tenders_by_site'][site] = stats['tenders_by_site'].get(site, 0) + 1
                
                # Group by month
                date = tender['date_limite']
                if date != 'N/A':
                    month = date.split('/')[1] if '/' in date else date.split(' ')[1]
                    stats['tenders_by_date'][month] = stats['tenders_by_date'].get(month, 0) + 1
            
            return Response(stats)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate statistics: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )