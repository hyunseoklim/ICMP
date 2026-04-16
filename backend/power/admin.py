from django.contrib import admin
from .models import PowerReading


@admin.register(PowerReading)
class PowerReadingAdmin(admin.ModelAdmin):
    list_display  = ('device', 'channel', 'current', 'voltage', 'power_usage', 'relay_state', 'measured_at')
    list_filter   = ('relay_state', 'channel', 'device')
    search_fields = ('device__device_id', 'channel')
    readonly_fields = ('measured_at',)
