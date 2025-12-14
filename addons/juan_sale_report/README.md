# Módulo: Informe de Pedido de Venta Personalizado

## Descripción
Módulo personalizado que añade un informe PDF customizado para pedidos de venta en Odoo 18.

## Características
- Diseño personalizado del informe de pedido de venta
- Colores y estilos personalizados
- Información adicional en el informe
- Pie de página customizado

## Instalación

1. El módulo ya está en la carpeta `addons/custom_sale_report`
2. Reinicia Odoo para que detecte el módulo:
   ```bash
   docker-compose restart web
   ```
3. Activa el modo desarrollador en Odoo:
   - Ir a Ajustes → Activar el modo de desarrollador
4. Actualiza la lista de aplicaciones:
   - Aplicaciones → Actualizar lista de aplicaciones
5. Busca "Informe de Pedido de Venta Personalizado" e instálalo

## Uso
Una vez instalado, ve a Ventas → Pedidos, abre un pedido y verás un nuevo botón de impresión con tu informe personalizado.

## Personalización
Puedes editar el archivo `views/sale_report_template.xml` para:
- Cambiar colores y estilos
- Añadir o quitar campos
- Modificar la estructura del informe
- Añadir tu logo de empresa

Después de cada cambio, actualiza el módulo desde Odoo.
