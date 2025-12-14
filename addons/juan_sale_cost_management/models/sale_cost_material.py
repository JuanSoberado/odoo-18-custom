# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleCostMaterial(models.Model):
    _name = 'sale.cost.material'
    _description = 'Material de Coste'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Secuencia', default=10)
    sale_line_id = fields.Many2one('sale.order.line', string='Línea de Venta', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    quantity = fields.Float(string='Cantidad', default=1.0, digits='Product Unit of Measure')
    uom_id = fields.Many2one('uom.uom', string='Unidad', related='product_id.uom_id', readonly=True)
    price_unit = fields.Float(string='Precio Unit.', digits='Product Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    notes = fields.Text(string='Notas')

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.standard_price
