from django.urls import path
from . import views

urlpatterns = [
    path('', views.workers_list, name='workers-list'),
    path('notify/', views.send_notification, name='send-notification'),
]
