from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/',       include('accounts.urls')),
    path('api/monitoring/', include('monitoring.urls')),
    path('api/gas/',        include('gas.urls')),
    path('api/power/',      include('power.urls')),
    path('api/workers/',    include('workers.urls')),
    path('api/events/',     include('events.urls')),
    path('api/safety/',     include('safety.urls')),
]
