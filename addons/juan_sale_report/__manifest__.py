{
    'name': 'Juan - Sale Report',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Informe personalizado para pedidos de venta',
    'description': """
        Módulo personalizado para informes de pedidos de venta
        ========================================================
        * Informe PDF personalizado
        * Diseño customizado
    """,
    'author': 'Juan Soberado',
    'depends': ['sale'],
    'data': [
        'views/sale_report_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
