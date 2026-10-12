"""
URL configuration for tienda_project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Toda la API de compras vive bajo /api/v1/
    path('api/v1/', include('compras.urls')),
]
