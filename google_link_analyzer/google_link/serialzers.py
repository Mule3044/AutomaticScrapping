from rest_framework import serializers 
from .models import google_link_analyzer


class google_link_analyzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = google_link_analyzer
        fields = '__all__'