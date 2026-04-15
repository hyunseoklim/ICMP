from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events-list'),
    path('<int:no>/', views.event_detail, name='event-detail'),
]
