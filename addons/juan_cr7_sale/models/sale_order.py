# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Override para mostrar a CR7 al confirmar"""
        res = super().action_confirm()
        
        # Mostrar wizard con CR7
        return {
            'name': '🎉 ¡SIUUUUUUU! 🎉',
            'type': 'ir.actions.act_window',
            'res_model': 'cr7.celebration.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_name': self.name,
                'default_message': '¡Otra venta pedazo de Anarco Capitalista! SIUUUUUUU',
            },
        }

