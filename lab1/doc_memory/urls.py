from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocumentoViewSet, MemoriaDocumentoViewSet,
    ReferenciaCruzadaViewSet, BusquedaDocumentoViewSet
)

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet)
router.register(r'memorias', MemoriaDocumentoViewSet)
router.register(r'referencias', ReferenciaCruzadaViewSet)
router.register(r'busquedas', BusquedaDocumentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
