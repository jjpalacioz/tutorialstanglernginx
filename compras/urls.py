from django.urls import path
from . import views
from .api.views import CompraAPIView

urlpatterns = [
    # Tutorial 03: API DRF (Controlador). Resuelve en /api/v1/comprar/
    # Procesa compras via JSON reutilizando el Service Layer.
    path('comprar/', CompraAPIView.as_view(), name='api_comprar'),

    # Tutorial 05: vista de salud/estado original (GET). /api/v1/estado/
    path('estado/', views.comprar, name='estado'),

    # Tutorial 03: vista HTML/JSON de inventario. /api/v1/inventario/
    # Permite ver como el stock cambia tras comprar por la API.
    path('inventario/', views.inventario, name='inventario'),
]
