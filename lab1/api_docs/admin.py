from django.contrib import admin
from .models import EndpointDoc


@admin.register(EndpointDoc)
class EndpointDocAdmin(admin.ModelAdmin):
    list_display = ('path', 'method', 'titulo', 'categoria', 'activo', 'updated_at')
    list_filter = ('method', 'categoria', 'activo')
    search_fields = ('path', 'titulo')
