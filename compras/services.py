from .domain.builders import OrdenBuilder
from .models import Producto


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: Semantica clara y validacion interna
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_productos(lista_productos)
                 .para_envio(direccion)
                 .build())

        # Uso del Factory (inyectado): Cambio de comportamiento
        # sin cambio de codigo
        if self.procesador.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")

    def ejecutar_compra(self, libro_id, direccion, usuario):
        """
        Logica de negocio de compra por UNIDAD de inventario (Tutorial 03).

        Esta es la MISMA logica de negocio que puede invocar tanto una vista
        HTML como la API DRF (demuestra la reutilizacion del Service Layer).

        Pasos:
          1. Busca el producto y valida que exista stock.
          2. Descuenta inventario (el cambio se refleja en la vista HTML).
          3. Ensambla la Orden con el Builder.
          4. Procesa el pago con el Factory (genera el log de pago).
        """
        # 1. Buscar producto (en el tutorial se llama 'libro', aqui 'producto')
        try:
            producto = Producto.objects.get(id=libro_id)
        except Producto.DoesNotExist:
            raise ValueError(f"El producto con id={libro_id} no existe.")

        # 2. Validacion de negocio: debe haber stock disponible
        if producto.stock <= 0:
            raise ValueError(f"Sin stock disponible para '{producto.nombre}'.")

        # 3. Descontar inventario (esto es lo que vera reflejado la vista HTML)
        producto.stock -= 1
        producto.save()

        # 4. Ensamblar la orden con el Builder
        orden = (self.builder
                 .con_usuario(str(usuario))
                 .con_productos([producto])
                 .para_envio(direccion)
                 .build())

        # 5. Procesar el pago con el Factory (genera el log [DEBUG]/[BANCO])
        if self.procesador.pagar(orden.total):
            return orden.total

        # Si el pago falla, revertimos: devolvemos el stock y borramos la orden
        producto.stock += 1
        producto.save()
        orden.delete()
        raise Exception("Error en la pasarela de pagos.")
