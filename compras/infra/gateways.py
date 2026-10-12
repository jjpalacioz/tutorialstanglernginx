"""
Gateways de infraestructura (pasarelas de pago reales).

Representan la "infraestructura real" que la aplicacion usa en produccion.
La Fabrica (factories.py) decide cual instanciar segun el entorno.
"""


class BancoNacionalProcesador:
    """Procesador de pagos de produccion (infraestructura real)."""

    def pagar(self, monto: float) -> bool:
        print(f"[BANCO] Procesando pago REAL de ${monto} con Banco Nacional.")
        # Aqui iria la integracion real con la pasarela del banco.
        return True
