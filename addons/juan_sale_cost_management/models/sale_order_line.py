# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    material_ids = fields.One2many('sale.cost.material', 'sale_line_id', string='Materiales')
    labor_ids = fields.One2many('sale.cost.labor', 'sale_line_id', string='Mano de Obra')
    
    # Campo computado para mostrar botón
    has_costs = fields.Boolean(compute='_compute_has_costs', string='Tiene Costes')
    
    @api.depends('material_ids', 'labor_ids')
    def _compute_has_costs(self):
        for line in self:
            line.has_costs = bool(line.material_ids or line.labor_ids)

    def action_view_costs(self):
        """Abrir ventana con materiales y mano de obra"""
        self.ensure_one()
        return {
            'name': f'Costes - {self.product_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('juan_sale_cost_management.view_sale_order_line_cost_form').id,
            'target': 'new',
        }
