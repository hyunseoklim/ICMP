from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_summary, name='dashboard-summary'),
    path('map/', views.realtime_map, name='realtime-map'),
]
