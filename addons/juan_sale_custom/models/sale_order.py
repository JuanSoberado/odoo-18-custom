# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    juan_comentarios_adicionales = fields.Char(
        string='Comentarios Adicionales',
        help='Comentarios adicionales para el pedido de venta'
    )
