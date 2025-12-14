# Guía de Módulos Personalizados - Odoo 18

## 📋 Índice
1. [juan_sale_custom - Campos Personalizados en Ventas](#juan_sale_custom)
2. [juan_sale_cost_management - Gestión de Materiales y Mano de Obra](#juan_sale_cost_management)
3. [juan_invoice_custom - Personalización de Facturas](#juan_invoice_custom)
4. [juan_due_list_bank - Campo Banco en Lista de Efectos](#juan_due_list_bank)

---

## juan_sale_custom

### 🎯 Objetivo
Agregar campos personalizados al formulario de pedidos de venta para capturar información adicional del negocio.

### 📝 ¿Qué hace?
- Agrega 3 campos nuevos en el pedido de venta:
  - **Campo Texto**: Para notas o referencias personalizadas
  - **Campo Fecha**: Para fechas específicas del pedido
  - **Campo Numérico**: Para valores cuantitativos adicionales

### 🔧 Implementación Técnica

**Archivo: `models/sale_order.py`**
```python
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Heredamos el modelo existente
    
    # Definimos los campos nuevos
    custom_text = fields.Char(string='Campo de Texto Personalizado')
    custom_date = fields.Date(string='Fecha Personalizada')
    custom_number = fields.Float(string='Número Personalizado')
```

**Archivo: `views/sale_order_views.xml`**
```xml
<xpath expr="//field[@name='payment_term_id']" position="after">
    <field name="custom_text"/>
    <field name="custom_date"/>
    <field name="custom_number"/>
</xpath>
```

### 💡 Explicación para Consultor Funcional

**¿Por qué se hizo así?**
- Usamos **herencia de modelos** (`_inherit`) para NO modificar el código base de Odoo
- Los campos se agregan después del campo "Plazos de pago" (`payment_term_id`)
- Los datos se guardan automáticamente en la base de datos sin necesidad de código adicional

**¿Qué puedes personalizar fácilmente?**
- Cambiar el nombre visible de los campos (el `string`)
- Agregar más campos copiando la estructura
- Mover los campos a otra posición cambiando el `xpath`
- Hacerlos obligatorios agregando `required="1"`

**Casos de uso:**
- Agregar número de orden de compra del cliente
- Capturar fecha de entrega requerida
- Registrar porcentaje de descuento especial

---

## juan_sale_cost_management

### 🎯 Objetivo
Gestionar materiales y mano de obra por cada línea de pedido de venta, con creación automática de tareas en proyectos.

### 📝 ¿Qué hace?
1. Agrega pestañas "Materiales" y "Mano de Obra" en cada línea del pedido
2. Permite registrar múltiples materiales con cantidades y precios
3. Permite registrar múltiples recursos de mano de obra con horas y tarifas
4. Al confirmar el pedido, crea automáticamente tareas en el proyecto asociado

### 🔧 Implementación Técnica

**Modelos Creados:**

1. **`sale.cost.material`** - Tabla de materiales
```python
class SaleCostMaterial(models.Model):
    _name = 'sale.cost.material'
    
    order_line_id = fields.Many2one('sale.order.line')  # Relación con línea
    product_id = fields.Many2one('product.product')      # Producto material
    quantity = fields.Float('Cantidad')
    unit_price = fields.Float('Precio Unitario')
    subtotal = fields.Float(compute='_compute_subtotal') # Calculado automático
```

2. **`sale.cost.labor`** - Tabla de mano de obra
```python
class SaleCostLabor(models.Model):
    _name = 'sale.cost.labor'
    
    order_line_id = fields.Many2one('sale.order.line')
    employee_id = fields.Many2one('hr.employee')  # Empleado
    hours = fields.Float('Horas')
    hourly_rate = fields.Float('Tarifa por Hora')
    subtotal = fields.Float(compute='_compute_subtotal')
```

3. **Extensión de `sale.order.line`**
```python
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # Relaciones One2many (un pedido → muchos materiales/mano de obra)
    material_ids = fields.One2many('sale.cost.material', 'order_line_id')
    labor_ids = fields.One2many('sale.cost.labor', 'order_line_id')
```

4. **Creación automática de tareas**
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        res = super().action_confirm()
        # Para cada línea que tenga mano de obra
        for line in self.order_line.filtered(lambda l: l.labor_ids):
            # Crear una tarea en el proyecto
            self.env['project.task'].create({
                'name': f'Trabajo: {line.product_id.name}',
                'project_id': self.project_id.id,
                'sale_line_id': line.id,
            })
        return res
```

### 💡 Explicación para Consultor Funcional

**Flujo de Trabajo:**

1. **Creación del Pedido:**
   - Usuario crea pedido de venta normal
   - Agrega líneas de producto

2. **Configuración de Costos:**
   - En cada línea, puede ir a pestaña "Materiales"
   - Agrega productos que se necesitan (ej: tornillos, madera, pintura)
   - Especifica cantidades y precios unitarios
   - El subtotal se calcula solo: `cantidad × precio`

3. **Asignación de Mano de Obra:**
   - Va a pestaña "Mano de Obra"
   - Selecciona empleados que trabajarán
   - Indica horas estimadas y tarifa por hora
   - Subtotal automático: `horas × tarifa`

4. **Confirmación y Automatización:**
   - Al confirmar pedido, si tiene proyecto asignado
   - Se crean tareas automáticas por cada línea con mano de obra
   - Las tareas incluyen referencia al pedido

**Ventajas del Diseño:**

✅ **Trazabilidad**: Sabes exactamente qué materiales y personas van a cada servicio
✅ **Costeo**: Puedes calcular el costo real vs precio de venta
✅ **Planificación**: Las tareas se crean solas, no hay que recordar crearlas
✅ **Flexibilidad**: Cada línea puede tener diferentes recursos

**Personalización Fácil:**
- Agregar campos adicionales (ej: proveedor del material)
- Cambiar cálculo de subtotal (ej: aplicar descuento)
- Modificar qué crea la tarea (ej: asignar empleado automáticamente)

---

## juan_invoice_custom

### 🎯 Objetivo
Mover el campo "Banco Destinatario" a la vista principal de la factura para facilitar su acceso y hacerlo disponible en vistas relacionadas.

### 📝 ¿Qué hace?
1. Reubica el campo banco de la pestaña "Otra Información" a la sección principal
2. Crea un campo relacionado en líneas contables para usar en otras vistas
3. Muestra el banco justo debajo del campo "Cliente"

### 🔧 Implementación Técnica

**1. Personalización de Vista de Factura**

**Archivo: `views/account_move_views.xml`**
```xml
<!-- Ocultar banco de la ubicación original -->
<xpath expr="//field[@name='partner_bank_id']" position="attributes">
    <attribute name="invisible">1</attribute>
</xpath>

<!-- Mostrar banco debajo del cliente -->
<xpath expr="//field[@name='partner_id']" position="after">
    <field name="partner_bank_id" 
           string="Banco Destinatario"
           domain="[('partner_id', '=', partner_id)]"/>
</xpath>
```

**2. Campo Relacionado en Líneas Contables**

**Archivo: `models/account_move_line.py`**
```python
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        related='move_id.partner_bank_id',  # Toma el valor de la factura
        string='Banco Destinatario',
        store=True,   # Se guarda en BD para búsquedas rápidas
        readonly=True  # No se puede editar desde aquí
    )
```

### 💡 Explicación para Consultor Funcional

**¿Por qué es importante?**

Antes: El campo banco estaba "escondido" en la pestaña "Otra Información"
- Usuario tenía que hacer scroll y buscar
- No estaba visible al crear/editar factura rápidamente

Ahora: El campo banco está en la vista principal
- Visible inmediatamente debajo del cliente
- Filtrado automáticamente: solo muestra bancos de ese cliente
- Accesible desde apuntes contables para reportes

**Flujo de Usuario:**

1. Usuario crea factura de cliente
2. Selecciona el cliente
3. Inmediatamente debajo aparece campo "Banco Destinatario"
4. Desplegable muestra solo cuentas bancarias de ese cliente
5. Selecciona banco y continúa

**Ventaja del Campo Relacionado:**

El campo `partner_bank_id` ahora existe en `account.move.line`:
- ✅ Se puede usar en filtros de búsqueda
- ✅ Aparece en exportaciones a Excel
- ✅ Disponible para reportes personalizados
- ✅ Se puede agrupar por banco en listas

**Detalles Técnicos Importantes:**
- `domain` = Solo muestra bancos del cliente seleccionado
- `related` = El valor viene automáticamente de la factura padre
- `store=True` = Mejora rendimiento en búsquedas
- `readonly=True` = Evita inconsistencias (se edita solo en factura)

---

## juan_due_list_bank

### 🎯 Objetivo
Agregar el campo "Banco Destinatario" a la vista de Efectos (Payments and due list) con capacidad de filtrado y agrupación.

### 📝 ¿Qué hace?
1. Muestra columna "Banco Destinatario" en lista de efectos
2. Permite buscar por banco en el panel de búsqueda
3. Permite agrupar efectos por banco destinatario
4. NO modifica módulos OCA, crea extensión limpia

### 🔧 Implementación Técnica

**Dependencias Clave:**
```python
'depends': ['account_due_list', 'juan_invoice_custom']
```
- `account_due_list`: Módulo OCA que crea la vista de efectos
- `juan_invoice_custom`: Nuestro módulo que creó el campo relacionado

**Estructura del Módulo:**

**1. Heredar Vista de Lista**
```xml
<record id="view_payments_tree_bank" model="ir.ui.view">
    <field name="inherit_id" ref="account_due_list.view_payments_tree"/>
    <field name="arch" type="xml">
        <!-- Agregar columna después de Ref. Cliente -->
        <xpath expr="//field[@name='partner_ref']" position="after">
            <field name="partner_bank_id" 
                   string="Banco Destinatario" 
                   readonly="1" 
                   optional="show"/>
        </xpath>
    </field>
</record>
```

**2. Heredar Vista de Búsqueda**
```xml
<record id="view_payments_filter_bank" model="ir.ui.view">
    <field name="inherit_id" ref="account_due_list.view_payments_filter"/>
    <field name="arch" type="xml">
        <!-- Agregar campo de búsqueda -->
        <xpath expr="//field[@name='payment_term_id']" position="after">
            <field name="partner_bank_id"/>
        </xpath>
        
        <!-- Agregar opción de agrupar -->
        <xpath expr="//filter[@name='group_by_salesperson']" position="after">
            <filter string="Banco Destinatario" 
                    name="group_by_bank" 
                    context="{'group_by':'partner_bank_id'}"/>
        </xpath>
    </field>
</record>
```

### 💡 Explicación para Consultor Funcional

**¿Por qué un módulo separado?**

**Problema:** El módulo `account_due_list` es de OCA (comunidad)
- Si lo modificamos directamente, perdemos los cambios al actualizar
- Conflictos con otros que usen el mismo módulo

**Solución:** Crear módulo de extensión
- `juan_due_list_bank` depende de `account_due_list`
- Hereda sus vistas sin tocar su código
- Se puede actualizar OCA sin problemas

**¿Cómo funciona la herencia de vistas?**

Odoo combina vistas usando `xpath`:
```
Vista Original OCA        →  Nuestra Extensión    →   Vista Final
[Fecha, Cliente, Ref]        + [Banco]               [Fecha, Cliente, Ref, Banco]
```

**Flujo de Usuario en Efectos:**

1. **Ver la Columna:**
   - Usuario va a Contabilidad → Efectos
   - Ve columna "Banco Destinatario" (oculta por defecto)
   - Puede activarla desde el menú de columnas

2. **Buscar por Banco:**
   - Hace clic en buscador superior
   - Escribe nombre del banco
   - Filtra solo efectos de ese banco

3. **Agrupar por Banco:**
   - Hace clic en "Agrupar por"
   - Selecciona "Banco Destinatario"
   - Ve efectos organizados por banco con totales

**Atributos Importantes:**

- `optional="show"`: Columna visible por defecto (puede ser "hide")
- `readonly="1"`: No se puede editar desde aquí (viene de factura)
- `position="after"`: Define dónde insertar el campo
- `context={'group_by':'partner_bank_id'}`: Configuración para agrupación

**Casos de Uso:**

✅ **Tesorería:** "Quiero ver todos los pagos que van al Banco Santander"
✅ **Reconciliación:** "Agrupar efectos por banco para cuadrar extractos"
✅ **Reporting:** "Exportar lista de efectos con banco destinatario"

---

## 🔄 Relación Entre Módulos

```
juan_invoice_custom
        ↓
    (crea campo partner_bank_id en account.move.line)
        ↓
juan_due_list_bank
        ↓
    (usa ese campo en vista de efectos)
```

**Dependencias:**
1. `juan_invoice_custom` debe instalarse PRIMERO
2. Luego se puede instalar `juan_due_list_bank`
3. Los otros módulos son independientes

---

## 📊 Mejores Prácticas Aplicadas

### 1. **Herencia sin Modificación**
❌ NO: Editar archivos de Odoo estándar
✅ SÍ: Usar `_inherit` para extender

### 2. **Campos Relacionados**
❌ NO: Duplicar datos
✅ SÍ: Usar `related` con `store=True`

### 3. **Módulos Separados**
❌ NO: Un módulo gigante que hace todo
✅ SÍ: Módulos pequeños con funciones específicas

### 4. **XPath Precisos**
❌ NO: `//field` (muy genérico)
✅ SÍ: `//field[@name='campo_especifico']`

### 5. **Dependencias Claras**
Siempre especificar en `__manifest__.py`:
```python
'depends': ['sale', 'project', 'hr']
```

---

## 🛠️ Comandos Útiles para Consultor

### Actualizar Módulo
```bash
# Reiniciar Odoo
docker-compose restart web

# O desde interfaz:
Aplicaciones → Buscar módulo → Actualizar
```

### Ver Logs de Error
```bash
docker-compose logs -f web
```

### Limpiar Caché del Navegador
```
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

---

## 📞 Soporte y Personalización

**Para modificar estos módulos:**
1. Edita los archivos Python/XML
2. Actualiza el módulo en Odoo
3. Recarga la página con F5

**Recuerda:**
- Siempre hacer backup antes de cambios grandes
- Probar en base de datos de prueba primero
- Documentar cambios personalizados

---

**Autor:** Juan Soberado
**Fecha:** Diciembre 2025
**Versión Odoo:** 18.0
