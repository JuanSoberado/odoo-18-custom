# -*- coding: utf-8 -*-
{
    'name': 'Juan - Due List Bank Field',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Agregar campo banco destinatario a la lista de efectos',
    'description': """
        Agregar campo banco destinatario a la lista de efectos
        ======================================================
        * Agrega el campo partner_bank_id a la vista de efectos
        * Incluye filtros y agrupación por banco
    """,
    'author': 'Juan Soberado',
    'depends': ['account_due_list', 'juan_invoice_custom'],
    'data': [
        'views/payment_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
