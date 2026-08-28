from rest_framework import serializers
from .models import QueryLog, IndexRecommendation, DatabaseStats, TableStats


class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = '__all__'


class IndexRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexRecommendation
        fields = '__all__'


class DatabaseStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseStats
        fields = '__all__'


class TableStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableStats
        fields = '__all__'
