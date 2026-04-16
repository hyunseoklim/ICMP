from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.power_devices_list, name='power-devices-list'),
    path('devices/<str:device_id>/', views.power_device_detail, name='power-device-detail'),
]
