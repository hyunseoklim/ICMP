from django.contrib import admin
from .models import EnvironmentData


@admin.register(EnvironmentData)
class EnvironmentDataAdmin(admin.ModelAdmin):
    list_display  = ('device_id', 'temp', 'humi', 'lat', 'lon', 'timestamp')
    list_filter   = ('device_id',)
    search_fields = ('device_id',)
    readonly_fields = ('timestamp',)
