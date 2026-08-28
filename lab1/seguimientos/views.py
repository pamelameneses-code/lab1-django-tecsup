from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Proyecto, Tarea, Comentario, HistorialCambio
from .serializers import (
    ProyectoSerializer, TareaSerializer,
    ComentarioSerializer, HistorialCambioSerializer
)


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    @action(detail=False, methods=['get'])
    def en_progreso(self, request):
        proyectos = self.queryset.filter(estado='en_progreso')
        serializer = self.get_serializer(proyectos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def resumen(self, request, pk=None):
        proyecto = self.get_object()
        return Response({
            'id': proyecto.id,
            'nombre': proyecto.nombre,
            'estado': proyecto.estado,
            'progreso': proyecto.progreso,
            'total_tareas': proyecto.tareas.count(),
            'tareas_completadas': proyecto.tareas.filter(estado='completada').count(),
        })


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        proyecto_id = self.request.query_params.get('proyecto')
        if proyecto_id:
            qs = qs.filter(proyecto_id=proyecto_id)
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        tarea = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in dict(Tarea.ESTADO_CHOICES):
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

        HistorialCambio.objects.create(
            tarea=tarea,
            usuario=request.user if request.user.is_authenticated else None,
            campo='estado',
            valor_anterior=tarea.estado,
            valor_nuevo=nuevo_estado
        )
        tarea.estado = nuevo_estado
        tarea.save()
        return Response({'status': nuevo_estado})


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer


class HistorialCambioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialCambio.objects.all()
    serializer_class = HistorialCambioSerializer
