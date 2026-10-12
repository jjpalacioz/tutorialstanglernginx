from django.urls import path
from . import views

urlpatterns = [
    # Resuelve en: /api/v1/comprar/
    path('comprar/', views.comprar, name='comprar'),
]
