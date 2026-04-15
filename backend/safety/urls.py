from django.urls import path
from . import views

urlpatterns = [
    path('checklist/', views.checklist_items, name='checklist-items'),
    path('checklist/submit/', views.submit_checklist, name='submit-checklist'),
    path('history/', views.safety_history, name='safety-history'),
    path('vr/progress/', views.save_vr_progress, name='vr-progress'),
    path('vr/complete/', views.complete_vr, name='vr-complete'),
]
