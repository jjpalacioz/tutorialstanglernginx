# Entrega — Tutorial 03: Introducción a APIs con DRF

Este documento explica **cómo generar la evidencia** que pide el tutorial y qué
subir a la plataforma. El código de la capa API ya está implementado y
verificado en este repositorio:

- `compras/api/serializers.py` → **Adapter / DTO** (`OrdenInputSerializer`, `ProductoSerializer`)
- `compras/api/views.py` → **Controlador** (`CompraAPIView`) que **reutiliza** `CompraService`
- `compras/urls.py` → ruta `POST /api/v1/comprar/`
- `compras/views.py` → vista de **inventario** (`GET /api/v1/inventario/`) para ver el stock
- `compras/infra/factories.py` → **Factory** que entrega el procesador de pago (genera el log)

> Idea arquitectónica: la API es solo **otra puerta** hacia la **misma lógica de
> negocio** (`CompraService`). La vista HTML y la API comparten el mismo Service Layer.

---

## 0. Requisitos

Activar el entorno virtual (o conda) donde ya tienes Django instalado:

```bash
pip install djangorestframework
```

(Para la demostración local puedes usar SQLite; en producción el proyecto usa
PostgreSQL vía Docker Compose. Las variables de BD están en `settings.py`.)

---

## 1. Preparar la base de datos y datos de prueba

```bash
python manage.py migrate
python manage.py seed_productos      # crea 3 productos con stock
```

Verás algo como:
```
Creado: Libro Clean Architecture (id=1, stock=10)
Creado: Libro Patrones GoF (id=2, stock=5)
Creado: Libro Refactoring (id=3, stock=8)
```

---

## 2. Ver el inventario ANTES de comprar (puerta HTML)

Levanta el servidor:
```bash
python manage.py runserver
```

Abre en el navegador: <http://localhost:8000/api/v1/inventario/>

Anota el `stock` del producto id=1 (p. ej. **stock: 10**). Toma captura.

---

## 3. Comprar por la API (puerta JSON) — EVIDENCIA PRINCIPAL

Usa **Postman** o la **interfaz web de DRF** y envía:

```
POST http://localhost:8000/api/v1/comprar/
Content-Type: application/json

{
    "libro_id": 1,
    "direccion_envio": "Calle 123 #45-67"
}
```

Respuesta esperada (HTTP 201):
```json
{
    "estado": "exito",
    "mensaje": "Orden creada. Total: 95200.0000"
}
```

> **Captura esta petición y su respuesta** (requisito del tutorial).

### Log de pagos (archivo de evidencia)
En la **terminal donde corre el servidor** aparecerá el log generado por la Factory:
```
[BANCO] Procesando pago REAL de $95200.0000 con Banco Nacional.
```
(o `[DEBUG] Mock Payment: ...` si exportaste `PAYMENT_PROVIDER=MOCK`).

Para guardar ese log en un archivo, arranca el servidor redirigiendo la salida:
```bash
python manage.py runserver 2>&1 | tee evidencia_log_pagos.txt
```

---

## 4. Ver el inventario DESPUÉS de comprar (misma habitación)

Recarga <http://localhost:8000/api/v1/inventario/>

El producto id=1 ahora tendrá **stock: 9** (bajó 1). Toma captura.

Esto demuestra que **comprar por la API** descontó inventario igual que lo haría
la web → ambas "puertas" conducen a la **misma lógica de negocio**.

---

## 5. Qué subir a la plataforma ("tutorial0-3 DRF&API")

1. **`evidencia_log_pagos.txt`** — el log de pagos generado por la Factory.
2. **Captura(s) de pantalla**:
   - El POST a `/api/v1/comprar/` con su respuesta 201 (Postman o DRF).
   - El inventario antes (stock 10) y después (stock 9) de la compra.

---

## Comportamiento rápido de prueba (opcional, con el shell)

Si quieres verificar la lógica sin HTTP:
```bash
python manage.py shell
```
```python
from compras.services import CompraService
from compras.infra.factories import PaymentFactory
from compras.models import Producto

p = Producto.objects.get(id=1)
print("Stock antes:", p.stock)

servicio = CompraService(procesador_pago=PaymentFactory.get_processor())
total = servicio.ejecutar_compra(libro_id=1, direccion="Calle 123", usuario="demo")
print("Total:", total)

print("Stock despues:", Producto.objects.get(id=1).stock)   # bajó 1
```
