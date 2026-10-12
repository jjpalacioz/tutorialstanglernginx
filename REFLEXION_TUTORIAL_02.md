# Reflexión — Tutorial 02: Patrones Creacionales

## ¿Por qué el `OrdenBuilder` reduce el riesgo de errores frente a crear la orden directamente en la vista?

El `OrdenBuilder` reduce el riesgo de errores porque **centraliza y encapsula** en un
solo lugar toda la lógica de construcción de una `Orden`: el cálculo del subtotal, la
aplicación del IVA (x1.19) y la validación de que existan un usuario y productos antes
de persistir el objeto. Si esa lógica estuviera escrita directamente en la vista, se
repetiría en cada punto donde se cree una orden, y cualquier cambio (por ejemplo, una
nueva tasa de impuesto o un campo obligatorio) obligaría a modificar múltiples lugares,
con el riesgo de olvidar alguno y generar órdenes inconsistentes. Además, su *fluent
interface* (`.con_usuario().con_productos().para_envio().build()`) hace el código
legible y autoexplicativo, y la validación interna del método `build()` impide crear
órdenes con datos insuficientes, lanzando un error controlado en lugar de guardar datos
corruptos en la base de datos. En resumen, el Builder convierte un proceso propenso a
errores y disperso en un flujo único, validado y reutilizable, dejando a la vista
"delgada" y enfocada solo en orquestar la petición.
