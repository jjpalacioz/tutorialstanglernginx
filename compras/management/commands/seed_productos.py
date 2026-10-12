from django.core.management.base import BaseCommand
from compras.models import Producto


class Command(BaseCommand):
    help = 'Carga productos de prueba para demostrar el inventario (Tutorial 03).'

    def handle(self, *args, **options):
        datos = [
            {'nombre': 'Libro Clean Architecture', 'precio': 80000, 'stock': 10},
            {'nombre': 'Libro Patrones GoF', 'precio': 95000, 'stock': 5},
            {'nombre': 'Libro Refactoring', 'precio': 70000, 'stock': 8},
        ]
        creados = 0
        for d in datos:
            obj, created = Producto.objects.get_or_create(
                nombre=d['nombre'],
                defaults={'precio': d['precio'], 'stock': d['stock']},
            )
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Creado: {obj.nombre} (id={obj.id}, stock={obj.stock})"
                    )
                )
            else:
                self.stdout.write(
                    f"Ya existia: {obj.nombre} (id={obj.id}, stock={obj.stock})"
                )
        self.stdout.write(self.style.SUCCESS(f"\nTotal nuevos productos: {creados}"))
