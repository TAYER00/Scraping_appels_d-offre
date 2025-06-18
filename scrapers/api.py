from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tender
from .serializers import TenderSerializer
from .services import TenderService

class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def list(self, request):
        # Import latest data from JSON
        TenderService.import_from_json()
        
        # Get all tenders
        tenders = self.get_queryset()
        serializer = self.get_serializer(tenders, many=True)
        
        return Response({
            'tenders': serializer.data,
            'last_updated': tenders.first().created_at if tenders.exists() else None
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        try:
            stats = TenderService.get_statistics()
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': f'Failed to generate statistics: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )