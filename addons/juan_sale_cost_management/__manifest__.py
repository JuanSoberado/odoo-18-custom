# -*- coding: utf-8 -*-
{
    'name': 'Juan - Sale Cost Management',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Gestión de costes: materiales y mano de obra en ventas',
    'description': """
        Gestión de Costes en Ventas
        ============================
        * Desglose de materiales por línea de venta
        * Definición de tareas de mano de obra
        * Creación automática de tareas en proyecto
        * Vista detallada con botón de acceso rápido
    """,
    'author': 'Juan Soberado',
    'depends': ['sale_management', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_cost_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
