from rest_framework import serializers
from .models import Documento, MemoriaDocumento, ReferenciaCruzada, BusquedaDocumento


class MemoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoriaDocumento
        fields = '__all__'


class ReferenciaCruzadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenciaCruzada
        fields = '__all__'


class DocumentoSerializer(serializers.ModelSerializer):
    memorias = MemoriaDocumentoSerializer(many=True, read_only=True)
    resumen = serializers.CharField(read_only=True)
    autor_nombre = serializers.CharField(source='autor.username', read_only=True, default=None)

    class Meta:
        model = Documento
        fields = '__all__'


class BusquedaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusquedaDocumento
        fields = '__all__'
