from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from .models import QueryLog, IndexRecommendation, DatabaseStats, TableStats
from .serializers import (
    QueryLogSerializer, IndexRecommendationSerializer,
    DatabaseStatsSerializer, TableStatsSerializer
)


class QueryLogViewSet(viewsets.ModelViewSet):
    queryset = QueryLog.objects.all()
    serializer_class = QueryLogSerializer

    @action(detail=False, methods=['get'])
    def slow_queries(self, request):
        slow = self.queryset.filter(is_slow=True)
        serializer = self.get_serializer(slow, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def analyze(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM django_query_log ORDER BY created_at DESC LIMIT 100")
            rows = cursor.fetchall()
        return Response({'analyzed': len(rows), 'message': 'Análisis completado'})


class IndexRecommendationViewSet(viewsets.ModelViewSet):
    queryset = IndexRecommendation.objects.all()
    serializer_class = IndexRecommendationSerializer

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        rec = self.get_object()
        rec.status = 'applied'
        rec.save()
        return Response({'status': 'applied', 'index': rec.index_name})

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = self.queryset.filter(status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class DatabaseStatsViewSet(viewsets.ModelViewSet):
    queryset = DatabaseStats.objects.all()
    serializer_class = DatabaseStatsSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        stats = self.queryset.first()
        if stats:
            serializer = self.get_serializer(stats)
            return Response(serializer.data)
        return Response({'message': 'No hay estadísticas disponibles'})

    @action(detail=False, methods=['post'])
    def capture(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM django_sql_log
            """)
        stats = DatabaseStats.objects.create(
            total_queries=0,
            slow_queries=0,
            avg_query_time=0,
        )
        serializer = self.get_serializer(stats)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableStatsViewSet(viewsets.ModelViewSet):
    queryset = TableStats.objects.all()
    serializer_class = TableStatsSerializer
