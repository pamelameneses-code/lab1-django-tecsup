from django.contrib import admin
from .models import QueryLog, IndexRecommendation, DatabaseStats, TableStats


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query_sql', 'duration_ms', 'is_slow', 'created_at')
    list_filter = ('is_slow', 'created_at')
    search_fields = ('query_sql',)


@admin.register(IndexRecommendation)
class IndexRecommendationAdmin(admin.ModelAdmin):
    list_display = ('index_name', 'table_name', 'priority', 'status', 'created_at')
    list_filter = ('priority', 'status')
    search_fields = ('table_name', 'index_name')


@admin.register(DatabaseStats)
class DatabaseStatsAdmin(admin.ModelAdmin):
    list_display = ('total_queries', 'slow_queries', 'avg_query_time', 'captured_at')


@admin.register(TableStats)
class TableStatsAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'row_count', 'table_size_mb', 'index_size_mb')
    search_fields = ('table_name',)
