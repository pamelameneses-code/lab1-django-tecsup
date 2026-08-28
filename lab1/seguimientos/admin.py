from django.contrib import admin
from .models import Proyecto, Tarea, Comentario, HistorialCambio


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'prioridad', 'creado_por', 'created_at')
    list_filter = ('estado', 'prioridad')
    search_fields = ('nombre',)
    filter_horizontal = ('participantes',)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'estado', 'asignado_a', 'fecha_limite')
    list_filter = ('estado', 'proyecto')
    search_fields = ('titulo',)
    filter_horizontal = ('dependencias',)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('tarea', 'autor', 'created_at')
    list_filter = ('created_at',)


@admin.register(HistorialCambio)
class HistorialCambioAdmin(admin.ModelAdmin):
    list_display = ('tarea', 'usuario', 'campo', 'valor_anterior', 'valor_nuevo', 'created_at')
    list_filter = ('campo', 'created_at')
