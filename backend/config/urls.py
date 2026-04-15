"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from monitoring import views as monitoring_views
from events import views as event_views
from safety import views as safety_views

# Template views (Django Template version)
urlpatterns = [
    # Auth
    path('', account_views.login_template_view, name='login'),
    path('login/', account_views.login_template_view, name='login'),
    path('logout/', account_views.logout_template_view, name='logout'),
    path('profile/', account_views.profile_template_view, name='profile'),

    # Main pages
    path('dashboard/', monitoring_views.dashboard_template_view, name='dashboard'),
    path('monitoring/realtime/', monitoring_views.realtime_monitoring_template_view, name='realtime_monitoring'),
    path('monitoring/gas/', monitoring_views.gas_monitoring_template_view, name='gas_monitoring'),
    path('monitoring/power/', monitoring_views.power_monitoring_template_view, name='power_monitoring'),
    path('monitoring/workers/', monitoring_views.workers_template_view, name='workers'),

    # Events
    path('events/', event_views.events_template_view, name='events'),
    path('events/<int:id>/', event_views.event_detail_template_view, name='event_detail'),

    # Safety
    path('safety/checklist/', safety_views.safety_checklist_template_view, name='safety_checklist'),
    path('safety/vr/', safety_views.safety_vr_template_view, name='safety_vr'),
    path('safety/history/', safety_views.safety_history_template_view, name='safety_history'),

    # Admin
    path('admin/', admin.site.urls),

    # API endpoints (REST)
    path('api/auth/', include('accounts.urls')),
    path('api/monitoring/', include('monitoring.urls')),
    path('api/events/', include('events.urls')),
    path('api/safety/', include('safety.urls')),
]

