from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/call/', include('apps.calls.urls')),
    path('v1/bill/', include('apps.bills.urls')),
]
