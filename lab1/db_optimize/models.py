from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class QueryLog(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    query_sql = models.TextField()
    duration_ms = models.FloatField()
    tables_involved = models.JSONField(default=list)
    is_slow = models.BooleanField(default=False)
    suggested_indexes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Query ({self.duration_ms}ms) - {self.query_sql[:80]}"


class IndexRecommendation(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('applied', 'Aplicada'),
        ('rejected', 'Rechazada'),
    ]

    table_name = models.CharField(max_length=255)
    index_name = models.CharField(max_length=255)
    columns = models.JSONField()
    index_type = models.CharField(max_length=50, default='btree')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField()
    estimated_improvement = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.index_name} on {self.table_name} ({self.priority})"


class DatabaseStats(models.Model):
    total_queries = models.IntegerField(default=0)
    slow_queries = models.IntegerField(default=0)
    avg_query_time = models.FloatField(default=0)
    total_rows_scanned = models.BigIntegerField(default=0)
    cache_hit_ratio = models.FloatField(default=0)
    recommendations_applied = models.IntegerField(default=0)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return f"Stats at {self.captured_at} - {self.total_queries} queries"


class TableStats(models.Model):
    table_name = models.CharField(max_length=255, unique=True)
    row_count = models.BigIntegerField(default=0)
    table_size_mb = models.FloatField(default=0)
    index_size_mb = models.FloatField(default=0)
    sequential_scans = models.IntegerField(default=0)
    index_scans = models.IntegerField(default=0)
    last_vacuum = models.DateTimeField(null=True, blank=True)
    last_analyze = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.table_name} - {self.row_count} rows"
