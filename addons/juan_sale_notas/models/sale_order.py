from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_notas_internas = fields.Text(
        string='Notas Internas',
        help='Notas Juannnnnn'
    )

    x_total_formateado = fields.Char(
        string='Total Formateado',
        compute='_compute_total_formateado',
        store=False
    )

    @api.depends('amount_total', 'currency_id')
    def _compute_total_formateado(self):
        for record in self:
            record.x_total_formateado = "Total: {:,.2f} {}".format(
                record.amount_total,
                record.currency_id.symbol or ''
            )
