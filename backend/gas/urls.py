from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.gas_sensors_list, name='gas-sensors-list'),
    path('sensors/<str:sensor_id>/', views.gas_sensor_detail, name='gas-sensor-detail'),
]
