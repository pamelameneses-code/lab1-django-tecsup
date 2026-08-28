from django.db import models
from django.contrib.auth.models import User


class Documento(models.Model):
    TIPO_CHOICES = [
        ('spec', 'Especificación'),
        ('design', 'Diseño'),
        ('api', 'Documentación API'),
        ('user_guide', 'Guía de Usuario'),
        ('changelog', 'Registro de Cambios'),
        ('meeting', 'Acta de Reunión'),
        ('report', 'Reporte'),
        ('other', 'Otro'),
    ]

    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='other')
    version = models.CharField(max_length=20, default='1.0')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='documentos')
    tags = models.JSONField(default=list)
    metadata = models.JSONField(default=dict)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.titulo} v{self.version}"

    @property
    def resumen(self):
        return self.contenido[:200] + '...' if len(self.contenido) > 200 else self.contenido


class MemoriaDocumento(models.Model):
    """Almacena la memoria/índice semántico de los documentos"""
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='memorias')
    clave = models.CharField(max_length=255)
    valor = models.TextField()
    contexto = models.TextField(blank=True)
    relevancia = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-relevancia', '-updated_at']
        unique_together = ['documento', 'clave']

    def __str__(self):
        return f"{self.clave}: {self.valor[:50]}"


class ReferenciaCruzada(models.Model):
    """Referencias entre documentos"""
    documento_origen = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='referencias_salida')
    documento_destino = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='referencias_entrada')
    tipo_relacion = models.CharField(max_length=50, default='referencia')
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['documento_origen', 'documento_destino']

    def __str__(self):
        return f"{self.documento_origen} → {self.documento_destino}"


class BusquedaDocumento(models.Model):
    """Historial de búsquedas para mejorar el motor de recomendación"""
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query = models.CharField(max_length=500)
    resultados_encontrados = models.IntegerField(default=0)
    documento_seleccionado = models.ForeignKey(Documento, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Búsquedas de documentos'

    def __str__(self):
        return f"Búsqueda: {self.query[:50]}"
