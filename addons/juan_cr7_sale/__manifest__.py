# -*- coding: utf-8 -*-
{
    'name': 'Juan - CR7 SIUUUU Sale Confirmation',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Cristiano Ronaldo celebra tus ventas - SIUUUU!',
    'description': """
        CR7 SIUUUU Sale Celebration
        ============================
        Muestra a Cristiano Ronaldo celebrando cada vez que confirmas un pedido
        ¡SIUUUUUUU Anarco Capitalista!
    """,
    'author': 'Juan Soberado',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/cr7_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'juan_cr7_sale/static/src/js/cr7_notification.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
