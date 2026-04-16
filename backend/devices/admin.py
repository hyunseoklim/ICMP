from django.contrib import admin
from .models import GasSensor, SmartPowerDevice


@admin.register(GasSensor)
class GasSensorAdmin(admin.ModelAdmin):
    list_display  = ('sensor_id', 'device_name', 'location', 'status', 'is_connected', 'created_at')
    list_filter   = ('status', 'is_connected')
    search_fields = ('sensor_id', 'location')


@admin.register(SmartPowerDevice)
class SmartPowerDeviceAdmin(admin.ModelAdmin):
    list_display  = ('device_id', 'device_name', 'status', 'is_connected', 'created_at')
    list_filter   = ('status', 'is_connected')
    search_fields = ('device_id', 'device_name')
