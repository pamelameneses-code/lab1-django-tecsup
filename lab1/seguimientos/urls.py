from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProyectoViewSet, TareaViewSet,
    ComentarioViewSet, HistorialCambioViewSet
)

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
router.register(r'tareas', TareaViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'historial', HistorialCambioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
