from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EndpointDocViewSet

router = DefaultRouter()
router.register(r'endpoints', EndpointDocViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
