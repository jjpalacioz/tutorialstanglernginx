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
