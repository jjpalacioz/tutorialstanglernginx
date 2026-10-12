from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='compras'
    )
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Compra #{self.pk} - {self.producto.nombre} x{self.cantidad}'


class Orden(models.Model):
    """
    Objeto de dominio complejo que se ensambla con el patron Builder
    (ver domain/builders.py). Agrupa usuario, total (con IVA) y la
    direccion de envio.
    """
    usuario = models.CharField(max_length=150)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    direccion_envio = models.CharField(max_length=255, blank=True, default='')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Orden #{self.pk} - {self.usuario} (${self.total})'
