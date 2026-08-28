from django.contrib import admin
from .models import Documento, MemoriaDocumento, ReferenciaCruzada, BusquedaDocumento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'version', 'autor', 'activo', 'updated_at')
    list_filter = ('tipo', 'activo')
    search_fields = ('titulo', 'contenido')


@admin.register(MemoriaDocumento)
class MemoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('documento', 'clave', 'relevancia', 'updated_at')
    list_filter = ('relevancia',)
    search_fields = ('clave', 'valor')


@admin.register(ReferenciaCruzada)
class ReferenciaCruzadaAdmin(admin.ModelAdmin):
    list_display = ('documento_origen', 'documento_destino', 'tipo_relacion', 'created_at')


@admin.register(BusquedaDocumento)
class BusquedaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('query', 'usuario', 'resultados_encontrados', 'created_at')
    search_fields = ('query',)
