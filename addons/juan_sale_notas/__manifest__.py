{
    'name': 'Notas en Pedidos de Venta',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Añade campo de notas internas y total formateado en pedidos de venta',
    'description': """
        Este módulo añade:
        - Campo de notas internas en pedidos de venta
        - Campo calculado con el total formateado
    """,
    'author': 'Juan Soberado',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
