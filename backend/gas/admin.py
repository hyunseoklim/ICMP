from django.contrib import admin
from .models import GasReading


@admin.register(GasReading)
class GasReadingAdmin(admin.ModelAdmin):
    list_display  = ('sensor', 'danger_level', 'o2', 'co', 'h2s', 'co2', 'measured_at')
    list_filter   = ('danger_level', 'sensor')
    search_fields = ('sensor__sensor_id',)
    readonly_fields = ('danger_level', 'measured_at')
