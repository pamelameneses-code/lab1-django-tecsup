from rest_framework import serializers
from .models import Proyecto, Tarea, Comentario, HistorialCambio


class HistorialCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialCambio
        fields = '__all__'


class ComentarioSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source='autor.username', read_only=True)

    class Meta:
        model = Comentario
        fields = '__all__'


class TareaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)
    historial = HistorialCambioSerializer(many=True, read_only=True)
    asignado_nombre = serializers.CharField(source='asignado_a.username', read_only=True, default=None)

    class Meta:
        model = Tarea
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    tareas = TareaSerializer(many=True, read_only=True)
    creado_por_nombre = serializers.CharField(source='creado_por.username', read_only=True, default=None)
    progreso = serializers.IntegerField(read_only=True)

    class Meta:
        model = Proyecto
        fields = '__all__'
