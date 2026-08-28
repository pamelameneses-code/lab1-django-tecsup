from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QueryLogViewSet, IndexRecommendationViewSet,
    DatabaseStatsViewSet, TableStatsViewSet
)

router = DefaultRouter()
router.register(r'queries', QueryLogViewSet)
router.register(r'recommendations', IndexRecommendationViewSet)
router.register(r'stats', DatabaseStatsViewSet)
router.register(r'tables', TableStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
