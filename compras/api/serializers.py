from rest_framework import serializers
from compras.models import Producto, Orden


class ProductoSerializer(serializers.ModelSerializer):
    """
    El Serializer es el patron Adapter aplicado a datos: transforma los
    modelos en JSON. (En el tutorial original el modelo se llama 'Libro';
    aqui usamos 'Producto' con su campo 'stock').
    """
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']


class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['id', 'usuario', 'total', 'direccion_envio', 'fecha']


class OrdenInputSerializer(serializers.Serializer):
    """
    Serializer para VALIDAR la entrada de datos, no necesariamente ligado
    a un modelo. Actua como un DTO (Data Transfer Object).
    """
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
    # Validaciones extras aqui si fueran necesarias
