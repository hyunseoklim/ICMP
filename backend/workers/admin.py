from django.contrib import admin
from .models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display  = ('worker_id', 'user', 'status', 'is_on_site', 'app_connected', 'last_connected')
    list_filter   = ('status', 'is_on_site', 'app_connected')
    search_fields = ('worker_id', 'user__first_name', 'user__last_name', 'user__username')
