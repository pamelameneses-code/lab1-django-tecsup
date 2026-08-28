from django.db import models


class EndpointDoc(models.Model):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
    ]

    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, default='general')
    parametros = models.JSONField(default=list)
    body_schema = models.JSONField(default=dict)
    response_schema = models.JSONField(default=dict)
    ejemplos = models.JSONField(default=list)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['path', 'method']
        unique_together = ['path', 'method']

    def __str__(self):
        return f"{self.method} {self.path}"
