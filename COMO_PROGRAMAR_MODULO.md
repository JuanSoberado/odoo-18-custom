# 🚀 Guía Completa: Cómo Programar un Módulo de Odoo desde Cero

## 📚 Índice
1. [Conceptos Básicos](#conceptos-básicos)
2. [Estructura de un Módulo](#estructura-de-un-módulo)
3. [Paso a Paso: Tu Primer Módulo](#paso-a-paso-tu-primer-módulo)
4. [Herencia de Modelos](#herencia-de-modelos)
5. [Vistas XML](#vistas-xml)
6. [Permisos y Seguridad](#permisos-y-seguridad)
7. [Debugging y Errores Comunes](#debugging-y-errores-comunes)
8. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Conceptos Básicos

### ¿Qué es un Módulo de Odoo?

Un módulo es como una **aplicación** que añades a Odoo para agregar o modificar funcionalidades. Es como instalar una app en tu móvil.

### Componentes de un Módulo

```
mi_modulo/
├── __init__.py          # Punto de entrada (importa todo)
├── __manifest__.py      # Información del módulo (como package.json)
├── models/              # Lógica de negocio (Python)
│   ├── __init__.py
│   └── mi_modelo.py
├── views/               # Interfaz de usuario (XML)
│   └── mi_vista.xml
└── security/            # Permisos (CSV)
    └── ir.model.access.csv
```

### Tecnologías que Necesitas Conocer

1. **Python** (80% del trabajo)
   - Clases y herencia
   - Decoradores básicos
   - Manejo de listas y diccionarios

2. **XML** (15% del trabajo)
   - Estructura básica
   - XPath para herencia

3. **PostgreSQL** (5% del trabajo)
   - Odoo lo maneja automáticamente

---

## Estructura de un Módulo

### 1. Archivo `__manifest__.py`

Este archivo es la **tarjeta de presentación** de tu módulo:

```python
{
    'name': 'Mi Primer Módulo',           # Nombre que verás en Aplicaciones
    'version': '18.0.1.0.0',              # Versión (Odoo.mayor.menor.parche)
    'category': 'Sales',                   # Categoría en el menú
    'summary': 'Resumen corto del módulo', # Descripción breve
    'description': """
        Descripción larga del módulo.
        Puede ser de varias líneas.
        Explica qué hace tu módulo.
    """,
    'author': 'Tu Nombre',                 # Tu nombre
    'website': 'https://www.tuempresa.com',
    'depends': [                           # Módulos que necesitas
        'base',                            # Siempre incluir 'base'
        'sale',                            # Si trabajas con ventas
        'account',                         # Si trabajas con contabilidad
    ],
    'data': [                              # Archivos que carga el módulo
        'security/ir.model.access.csv',    # Permisos primero
        'views/mi_vista.xml',              # Vistas después
    ],
    'installable': True,                   # Si se puede instalar
    'application': False,                  # Si es aplicación principal
    'auto_install': False,                 # Si se instala automáticamente
}
```

### 2. Archivo `__init__.py` (raíz)

```python
# -*- coding: utf-8 -*-
from . import models  # Importa la carpeta models
```

### 3. Archivo `models/__init__.py`

```python
# -*- coding: utf-8 -*-
from . import mi_modelo  # Importa cada archivo .py de models
```

---

## Paso a Paso: Tu Primer Módulo

### Ejemplo: Módulo para Agregar Notas a Clientes

Vamos a crear `mi_cliente_notas` que agrega un campo de notas a los clientes.

### PASO 1: Crear Estructura de Carpetas

```bash
cd /ruta/a/odoo/addons
mkdir mi_cliente_notas
cd mi_cliente_notas
mkdir models
mkdir views
mkdir security
```

### PASO 2: Crear `__init__.py` (raíz)

```python
# -*- coding: utf-8 -*-
from . import models
```

### PASO 3: Crear `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    'name': 'Notas de Cliente',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Agregar campo de notas a clientes',
    'description': """
        Este módulo agrega un campo de notas 
        al formulario de clientes para registrar 
        información adicional.
    """,
    'author': 'Juan Soberado',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

### PASO 4: Crear `models/__init__.py`

```python
# -*- coding: utf-8 -*-
from . import res_partner
```

### PASO 5: Crear `models/res_partner.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'  # Heredamos el modelo de clientes
    
    # Agregamos nuestro campo nuevo
    notas_internas = fields.Text(
        string='Notas Internas',
        help='Notas privadas sobre este cliente'
    )
```

### PASO 6: Crear `views/res_partner_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Heredar la vista del formulario de clientes -->
    <record id="view_partner_form_notas" model="ir.ui.view">
        <field name="name">res.partner.form.notas</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/>
        <field name="arch" type="xml">
            <!-- Agregar campo después del teléfono -->
            <xpath expr="//field[@name='phone']" position="after">
                <field name="notas_internas" placeholder="Escribe notas aquí..."/>
            </xpath>
        </field>
    </record>
</odoo>
```

### PASO 7: Crear `security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_res_partner_notas,access_res_partner_notas,base.model_res_partner,base.group_user,1,1,1,0
```

### PASO 8: Instalar el Módulo

```bash
# Reiniciar Odoo
docker-compose restart web

# En la interfaz de Odoo:
# 1. Ir a Aplicaciones
# 2. Quitar filtro "Aplicaciones"
# 3. Buscar "Notas de Cliente"
# 4. Click en Instalar
```

---

## Herencia de Modelos

### Tipos de Herencia

#### 1. Herencia Clásica (`_inherit` solo)

**Úsala cuando:** Quieres AGREGAR campos a un modelo existente

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Extiendes sale.order
    
    mi_campo_nuevo = fields.Char('Mi Campo')
```

**Resultado:** `sale.order` ahora tiene `mi_campo_nuevo`

#### 2. Herencia por Delegación (`_name` + `_inherit`)

**Úsala cuando:** Quieres CREAR un nuevo modelo basado en otro

```python
class MiDocumento(models.Model):
    _name = 'mi.documento'      # Nuevo modelo
    _inherit = 'mail.thread'    # Hereda funciones de mail.thread
    
    nombre = fields.Char('Nombre')
```

**Resultado:** Nuevo modelo `mi.documento` con funciones de seguimiento

---

## Tipos de Campos

### Campos Básicos

```python
from odoo import fields, models

class MiModelo(models.Model):
    _name = 'mi.modelo'
    
    # Texto corto
    nombre = fields.Char(
        string='Nombre',           # Etiqueta visible
        required=True,             # Obligatorio
        size=100,                  # Máximo 100 caracteres
        help='Texto de ayuda'      # Tooltip
    )
    
    # Texto largo
    descripcion = fields.Text(string='Descripción')
    
    # Número entero
    cantidad = fields.Integer(string='Cantidad', default=0)
    
    # Número decimal
    precio = fields.Float(
        string='Precio',
        digits=(10, 2)  # 10 dígitos totales, 2 decimales
    )
    
    # Booleano (checkbox)
    activo = fields.Boolean(string='Activo', default=True)
    
    # Fecha
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    
    # Fecha y hora
    fecha_hora = fields.Datetime(string='Fecha y Hora')
    
    # Selección (dropdown)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador')
```

### Campos Relacionales

```python
from odoo import fields, models

class MiModelo(models.Model):
    _name = 'mi.modelo'
    
    # Many2one (uno a muchos)
    # Un pedido → un cliente
    partner_id = fields.Many2one(
        'res.partner',              # Modelo relacionado
        string='Cliente',
        required=True,
        ondelete='cascade'          # Si borras cliente, borra esto
    )
    
    # One2many (muchos a uno) - INVERSO de Many2one
    # Un pedido → muchas líneas
    line_ids = fields.One2many(
        'mi.modelo.line',           # Modelo de líneas
        'order_id',                 # Campo Many2one en líneas
        string='Líneas'
    )
    
    # Many2many (muchos a muchos)
    # Un producto → muchas categorías
    # Una categoría → muchos productos
    category_ids = fields.Many2many(
        'product.category',         # Modelo relacionado
        string='Categorías'
    )
```

### Campos Computados

```python
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Campo que se calcula automáticamente
    total_lineas = fields.Integer(
        string='Total de Líneas',
        compute='_compute_total_lineas',  # Método que lo calcula
        store=True                         # Guardarlo en BD
    )
    
    @api.depends('order_line')  # Se recalcula cuando order_line cambia
    def _compute_total_lineas(self):
        for record in self:
            record.total_lineas = len(record.order_line)
```

---

## Vistas XML

### Estructura Básica de una Vista

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="mi_vista_form" model="ir.ui.view">
        <field name="name">mi.modelo.form</field>
        <field name="model">mi.modelo</field>
        <field name="arch" type="xml">
            <!-- Aquí va el diseño -->
        </field>
    </record>
</odoo>
```

### Tipos de Vistas

#### 1. Vista Formulario (form)

```xml
<form string="Mi Formulario">
    <sheet>
        <group>
            <group>
                <field name="nombre"/>
                <field name="fecha"/>
            </group>
            <group>
                <field name="precio"/>
                <field name="activo"/>
            </group>
        </group>
        <notebook>
            <page string="Detalles">
                <field name="descripcion"/>
            </page>
            <page string="Líneas">
                <field name="line_ids">
                    <list>
                        <field name="producto"/>
                        <field name="cantidad"/>
                    </list>
                </field>
            </page>
        </notebook>
    </sheet>
</form>
```

#### 2. Vista Lista (list/tree)

```xml
<list string="Mi Lista">
    <field name="nombre"/>
    <field name="fecha"/>
    <field name="precio" sum="Total"/>
    <field name="activo"/>
</list>
```

#### 3. Vista Búsqueda (search)

```xml
<search string="Buscar">
    <!-- Campos de búsqueda -->
    <field name="nombre"/>
    <field name="partner_id"/>
    
    <!-- Filtros -->
    <filter name="activos" string="Activos" 
            domain="[('activo', '=', True)]"/>
    <filter name="hoy" string="Hoy" 
            domain="[('fecha', '=', context_today())]"/>
    
    <!-- Agrupar por -->
    <group expand="0" string="Agrupar Por">
        <filter name="group_partner" string="Cliente" 
                context="{'group_by':'partner_id'}"/>
        <filter name="group_fecha" string="Fecha" 
                context="{'group_by':'fecha'}"/>
    </group>
</search>
```

### Herencia de Vistas con XPath

```xml
<record id="view_form_heredada" model="ir.ui.view">
    <field name="inherit_id" ref="modulo_base.vista_original"/>
    <field name="arch" type="xml">
        
        <!-- Agregar DESPUÉS de un campo -->
        <xpath expr="//field[@name='nombre']" position="after">
            <field name="mi_campo_nuevo"/>
        </xpath>
        
        <!-- Agregar ANTES de un campo -->
        <xpath expr="//field[@name='nombre']" position="before">
            <field name="mi_campo_nuevo"/>
        </xpath>
        
        <!-- REEMPLAZAR un campo -->
        <xpath expr="//field[@name='nombre']" position="replace">
            <field name="mi_campo_nuevo"/>
        </xpath>
        
        <!-- Agregar DENTRO de un elemento -->
        <xpath expr="//group[@name='grupo1']" position="inside">
            <field name="mi_campo_nuevo"/>
        </xpath>
        
        <!-- Modificar ATRIBUTOS -->
        <xpath expr="//field[@name='nombre']" position="attributes">
            <attribute name="readonly">1</attribute>
            <attribute name="required">1</attribute>
        </xpath>
        
    </field>
</record>
```

---

## Métodos Python Importantes

### Métodos CRUD

```python
class MiModelo(models.Model):
    _name = 'mi.modelo'
    
    # CREATE - Crear registro
    def crear_ejemplo(self):
        nuevo = self.env['mi.modelo'].create({
            'nombre': 'Prueba',
            'precio': 100.00
        })
        return nuevo
    
    # READ - Leer registros
    def leer_ejemplo(self):
        # Buscar todos
        todos = self.env['mi.modelo'].search([])
        
        # Buscar con condiciones
        filtrados = self.env['mi.modelo'].search([
            ('precio', '>', 100),
            ('activo', '=', True)
        ])
        
        # Buscar uno
        primero = self.env['mi.modelo'].search([], limit=1)
        
        # Buscar por ID
        registro = self.env['mi.modelo'].browse(5)
        
    # UPDATE - Actualizar
    def actualizar_ejemplo(self):
        registro = self.env['mi.modelo'].browse(5)
        registro.write({'precio': 200.00})
        
        # O directamente
        registro.precio = 200.00
    
    # DELETE - Eliminar
    def eliminar_ejemplo(self):
        registro = self.env['mi.modelo'].browse(5)
        registro.unlink()
```

### Sobrescribir Métodos

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        # Ejecutar el código original PRIMERO
        res = super().action_confirm()
        
        # Agregar tu lógica personalizada
        for order in self:
            # Tu código aquí
            print(f"Pedido {order.name} confirmado!")
        
        # Devolver resultado original
        return res
```

### Decoradores Importantes

```python
from odoo import api, fields, models

class MiModelo(models.Model):
    _name = 'mi.modelo'
    
    # @api.depends - Para campos computados
    total = fields.Float(compute='_compute_total')
    
    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('subtotal'))
    
    # @api.onchange - Ejecutar cuando un campo cambia en UI
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.direccion = self.partner_id.street
    
    # @api.constrains - Validaciones
    @api.constrains('precio')
    def _check_precio(self):
        for record in self:
            if record.precio < 0:
                raise ValidationError('El precio no puede ser negativo')
    
    # @api.model - Método de clase (no necesita self)
    @api.model
    def mi_metodo_estatico(self):
        # No opera sobre registros específicos
        return "Hola"
```

---

## Permisos y Seguridad

### Archivo `ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_mi_modelo_user,Mi Modelo Usuario,model_mi_modelo,base.group_user,1,1,1,0
access_mi_modelo_manager,Mi Modelo Manager,model_mi_modelo,base.group_system,1,1,1,1
```

**Explicación de columnas:**
- `id`: Identificador único
- `name`: Nombre descriptivo
- `model_id:id`: `model_` + nombre del modelo (con `_`)
- `group_id:id`: Grupo de usuarios
- `perm_read`: 1 = puede leer, 0 = no puede
- `perm_write`: 1 = puede editar
- `perm_create`: 1 = puede crear
- `perm_unlink`: 1 = puede eliminar

**Grupos comunes:**
- `base.group_user`: Usuario interno (todos)
- `base.group_system`: Administrador
- `sales_team.group_sale_salesman`: Vendedor
- `sales_team.group_sale_manager`: Jefe de ventas

---

## Debugging y Errores Comunes

### Ver Logs de Odoo

```bash
# Ver logs en tiempo real
docker-compose logs -f web

# Ver últimas 100 líneas
docker-compose logs --tail=100 web
```

### Errores Comunes y Soluciones

#### Error: "Field X does not exist"

**Causa:** El campo no está definido o hay error de tipeo

**Solución:**
```python
# Verifica que el campo existe
nombre = fields.Char(string='Nombre')  # ✅
nonbre = fields.Char(string='Nombre')  # ❌ Error de tipeo
```

#### Error: "ParseError while parsing XML"

**Causa:** Error en sintaxis XML

**Solución:**
- Verifica que todas las etiquetas cierren: `<field/>` o `<field></field>`
- Verifica comillas: `name="campo"` no `name='campo'`
- Usa validador XML online

#### Error: "No access rights"

**Causa:** Faltan permisos en `ir.model.access.csv`

**Solución:** Agregar línea con permisos correctos

#### Error: "Already exists with the same name"

**Causa:** Archivo XML con ID duplicado

**Solución:** Cambiar `id=` por uno único

### Debugging con IPython

```python
# En cualquier método Python
import ipdb; ipdb.set_trace()

# Ahora puedes inspeccionar variables:
# - self: el objeto actual
# - self.env: entorno de Odoo
# - self.env.user: usuario actual
```

---

## Ejemplos Prácticos Completos

### Ejemplo 1: Campo Calculado Simple

```python
# models/sale_order.py
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Campo que cuenta líneas
    numero_lineas = fields.Integer(
        string='Número de Líneas',
        compute='_compute_numero_lineas',
        store=True
    )
    
    @api.depends('order_line')
    def _compute_numero_lineas(self):
        for order in self:
            order.numero_lineas = len(order.order_line)
```

```xml
<!-- views/sale_order_views.xml -->
<xpath expr="//field[@name='payment_term_id']" position="after">
    <field name="numero_lineas" readonly="1"/>
</xpath>
```

### Ejemplo 2: Botón que Ejecuta Acción

```python
# models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_enviar_email_personalizado(self):
        for order in self:
            # Aquí tu lógica
            template = self.env.ref('mi_modulo.email_template_pedido')
            template.send_mail(order.id, force_send=True)
        
        # Mensaje de confirmación
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Email enviado correctamente',
                'type': 'success',
            }
        }
```

```xml
<!-- views/sale_order_views.xml -->
<xpath expr="//button[@name='action_confirm']" position="after">
    <button name="action_enviar_email_personalizado" 
            type="object" 
            string="Enviar Email" 
            class="btn-primary"/>
</xpath>
```

### Ejemplo 3: Nuevo Modelo Completo

```python
# models/mi_tarea.py
from odoo import fields, models

class MiTarea(models.Model):
    _name = 'mi.tarea'
    _description = 'Mis Tareas'
    _order = 'fecha_limite desc'
    
    name = fields.Char('Título', required=True)
    descripcion = fields.Text('Descripción')
    responsable_id = fields.Many2one('res.users', 'Responsable')
    fecha_limite = fields.Date('Fecha Límite')
    completada = fields.Boolean('Completada', default=False)
    prioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ], string='Prioridad', default='media')
    
    def action_marcar_completada(self):
        self.completada = True
```

---

## 🎯 Checklist: Antes de Instalar tu Módulo

- [ ] Todos los `__init__.py` existen
- [ ] `__manifest__.py` tiene todas las dependencias
- [ ] Archivos XML bien formateados (sin errores de sintaxis)
- [ ] `ir.model.access.csv` tiene permisos básicos
- [ ] Nombres de archivos en minúsculas con `_`
- [ ] Reiniciaste Odoo después de agregar el módulo
- [ ] Actualizaste lista de aplicaciones

---

## 📖 Recursos Adicionales

### Documentación Oficial
- https://www.odoo.com/documentation/18.0/developer.html

### Comandos Útiles

```bash
# Actualizar módulo desde terminal
docker-compose exec web odoo -u mi_modulo -d nombre_bd --stop-after-init

# Ver estructura de un modelo
docker-compose exec web odoo shell -d nombre_bd
>>> self.env['sale.order'].fields_get()

# Modo desarrollo (auto-reload)
docker-compose exec web odoo --dev=all
```

### Tips Finales

1. **Siempre usa herencia** (`_inherit`), nunca modifiques archivos de Odoo
2. **Nombra tus archivos consistentemente**: `modelo_linea.py`, no `linea.py`
3. **Usa IDs únicos** en XML: `mi_modulo_vista_form`
4. **Prueba en copia** de la base de datos primero
5. **Documenta tu código** con comentarios
6. **Versiona con Git** para no perder cambios

---

**¡Felicidades!** Ahora tienes todo lo necesario para crear tus propios módulos de Odoo 🎉

**Próximos Pasos:**
1. Crea un módulo simple siguiendo el ejemplo
2. Pruébalo en tu entorno
3. Agrega complejidad gradualmente
4. Consulta esta guía cuando tengas dudas

**Recuerda:** Todos los expertos empezaron con un "Hello World" 🚀
