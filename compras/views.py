from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .infra.factories import PaymentFactory
from .services import CompraService
from .models import Producto


def setup_service():
    """
    La vista es 'agnostica': no sabe que banco se usa, solo sabe que la
    Fabrica le entrega un procesador que funciona. (Factory Method)
    """
    # ANTES: gateway = BancoNacionalProcesador()
    # AHORA: Delegacion total a la Fabrica
    gateway = PaymentFactory.get_processor()
    return CompraService(procesador_pago=gateway)


@api_view(['GET', 'POST'])
def comprar(request):
    """
    Endpoint de la API de compras (v1).

    GET  -> informacion de salud del endpoint (evidencia Tutorial 05).
    POST -> ejecuta el proceso de compra usando los patrones creacionales
            Factory Method + Builder (Tutorial 02).

    Body esperado en POST (JSON):
        {
            "usuario": "juan",
            "productos_ids": [1, 2],   # opcional; si no, usa productos demo
            "direccion": "Calle 123"
        }
    """
    if request.method == 'POST':
        usuario = request.data.get('usuario', 'cliente_demo')
        direccion = request.data.get('direccion', 'Direccion de prueba 123')
        productos_ids = request.data.get('productos_ids', [])

        # Obtenemos productos reales si se enviaron ids; si no, usamos
        # objetos demo en memoria para no exigir datos previos en la BD.
        if productos_ids:
            lista_productos = list(Producto.objects.filter(id__in=productos_ids))
        else:
            lista_productos = _productos_demo()

        # Toda la logica de negocio se delega al Service Layer, que a su
        # vez usa el Builder (construccion) y el Factory (pago).
        service = setup_service()
        try:
            resultado = service.ejecutar_proceso_compra(
                usuario=usuario,
                lista_productos=lista_productos,
                direccion=direccion,
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(
            {'mensaje': resultado},
            status=status.HTTP_201_CREATED,
        )

    data = {
        'mensaje': 'API de compras v1 funcionando correctamente.',
        'servido_por': 'Django + Gunicorn detras de Nginx (Proxy Inverso)',
        'arquitectura': 'Nginx (puerto 80) -> Gunicorn (web:8000) -> PostgreSQL',
        'patrones': 'Factory Method (pago) + Builder (orden)',
        'metodo': request.method,
    }
    return Response(data, status=status.HTTP_200_OK)


class _ProductoDemo:
    """Producto en memoria para demostrar el flujo sin datos previos."""

    def __init__(self, precio):
        self.precio = precio


def _productos_demo():
    # Dos productos de ejemplo: subtotal 100000 -> con IVA (x1.19) = 119000
    return [_ProductoDemo(precio=60000), _ProductoDemo(precio=40000)]
