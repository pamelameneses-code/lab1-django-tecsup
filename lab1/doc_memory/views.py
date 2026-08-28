from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Documento, MemoriaDocumento, ReferenciaCruzada, BusquedaDocumento
from .serializers import (
    DocumentoSerializer, MemoriaDocumentoSerializer,
    ReferenciaCruzadaSerializer, BusquedaDocumentoSerializer
)


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(titulo__icontains=search)
        return qs

    @action(detail=True, methods=['get'])
    def memorias(self, request, pk=None):
        doc = self.get_object()
        memorias = doc.memorias.all()
        serializer = MemoriaDocumentoSerializer(memorias, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Parámetro q requerido'}, status=status.HTTP_400_BAD_REQUEST)

        resultados = self.queryset.filter(
            titulo__icontains=query
        ) | self.queryset.filter(
            contenido__icontains=query
        ) | self.queryset.filter(
            tags__contains=[query]
        )

        BusquedaDocumento.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            query=query,
            resultados_encontrados=resultados.count()
        )

        serializer = self.get_serializer(resultados.distinct(), many=True)
        return Response({'query': query, 'resultados': serializer.data})

    @action(detail=True, methods=['post'])
    def agregar_memoria(self, request, pk=None):
        doc = self.get_object()
        memoria = MemoriaDocumento.objects.create(
            documento=doc,
            clave=request.data.get('clave', ''),
            valor=request.data.get('valor', ''),
            contexto=request.data.get('contexto', ''),
            relevancia=request.data.get('relevancia', 1.0)
        )
        serializer = MemoriaDocumentoSerializer(memoria)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MemoriaDocumentoViewSet(viewsets.ModelViewSet):
    queryset = MemoriaDocumento.objects.all()
    serializer_class = MemoriaDocumentoSerializer


class ReferenciaCruzadaViewSet(viewsets.ModelViewSet):
    queryset = ReferenciaCruzada.objects.all()
    serializer_class = ReferenciaCruzadaSerializer


class BusquedaDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BusquedaDocumento.objects.all()
    serializer_class = BusquedaDocumentoSerializer
