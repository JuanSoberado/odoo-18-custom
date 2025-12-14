{
    'name': 'Juan - Invoice Custom',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Personalización de vistas de facturas',
    'description': """
        Personalización de vistas de facturas
        =====================================
        * Mover campo Banco Destinatario a vista principal
        * Campo banco en apuntes contables
    """,
    'author': 'Juan Soberado',
    'depends': ['account', 'account_due_list'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
