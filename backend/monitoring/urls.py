from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_summary, name='dashboard-summary'),
    path('map/', views.realtime_map, name='realtime-map'),
    path('gas-sensors/', views.gas_sensors_list, name='gas-sensors-list'),
    path('gas-sensors/<str:sensor_id>/', views.gas_sensor_detail, name='gas-sensor-detail'),
    path('power-devices/', views.power_devices_list, name='power-devices-list'),
    path('power-devices/<str:device_id>/', views.power_device_detail, name='power-device-detail'),
    path('workers/', views.workers_list, name='workers-list'),
    path('notifications/send/', views.send_notification, name='send-notification'),
]
