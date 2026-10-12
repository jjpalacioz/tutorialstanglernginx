from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def comprar(request):
    """
    Endpoint de la API de compras (v1).

    Sirve como evidencia de enrutamiento del Tutorial 05:
    debe ser accesible en http://<IP-EC2>/api/v1/comprar/ (SIN el puerto 8000),
    demostrando que Nginx enruta correctamente hacia Django/Gunicorn.
    """
    data = {
        'mensaje': 'API de compras v1 funcionando correctamente.',
        'servido_por': 'Django + Gunicorn detras de Nginx (Proxy Inverso)',
        'arquitectura': 'Nginx (puerto 80) -> Gunicorn (web:8000) -> PostgreSQL',
        'metodo': request.method,
    }

    if request.method == 'POST':
        data['mensaje'] = 'Compra recibida correctamente (demo).'
        data['payload_recibido'] = request.data
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(data, status=status.HTTP_200_OK)
