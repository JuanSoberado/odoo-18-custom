# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        related='move_id.partner_bank_id',
        string='Banco Destinatario',
        store=True,
        readonly=True
    )
