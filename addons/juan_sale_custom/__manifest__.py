{
    'name': 'Juan - Sale Custom',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Campos personalizados para pedidos de venta',
    'description': """
        Campos personalizados para pedidos de venta
        ============================================
        * Campo de comentarios adicionales
    """,
    'author': 'Juan Soberado',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
