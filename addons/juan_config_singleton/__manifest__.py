{
    'name': 'Control de Descuentos en Ventas',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Singleton que controla descuentos máximos en pedidos de venta',
    'description': """
        Configuración global (singleton) que:
        - Define el descuento máximo permitido
        - Valida descuentos en líneas de pedido
        - Impide guardar pedidos con descuentos excesivos
    """,
    'author': 'Juan Soberado',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/config_views.xml',
        'views/menu_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
