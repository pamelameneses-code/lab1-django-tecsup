from django.db import models
from django.contrib.auth.models import User


class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('planificacion', 'Planificación'),
        ('en_progreso', 'En Progreso'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificacion')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin_estimada = models.DateField(null=True, blank=True)
    fecha_fin_real = models.DateField(null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='proyectos_creados')
    participantes = models.ManyToManyField(User, blank=True, related_name='proyectos')
    prioridad = models.IntegerField(default=3, choices=[(1, 'Crítica'), (2, 'Alta'), (3, 'Media'), (4, 'Baja')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-prioridad', '-created_at']

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

    @property
    def progreso(self):
        tareas = self.tareas.count()
        if tareas == 0:
            return 0
        completadas = self.tareas.filter(estado='completada').count()
        return round((completadas / tareas) * 100)


class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('en_revision', 'En Revisión'),
        ('completada', 'Completada'),
        ('bloqueada', 'Bloqueada'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    dependencias = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='depende_de')
    fecha_limite = models.DateField(null=True, blank=True)
    horas_estimadas = models.FloatField(default=0)
    horas_reales = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha_limite', '-created_at']

    def __str__(self):
        return f"{self.titulo} ({self.get_estado_display()})"


class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comentario de {self.autor} en {self.tarea}"


class HistorialCambio(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    campo = models.CharField(max_length=100)
    valor_anterior = models.TextField(blank=True)
    valor_nuevo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Historial de cambios'

    def __str__(self):
        return f"{self.campo}: {self.valor_anterior} → {self.valor_nuevo}"
