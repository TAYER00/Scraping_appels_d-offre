from rest_framework import serializers
from .models import Tender

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'site', 'objet', 'date_limite', 'created_at', 'updated_at']