# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleCostLabor(models.Model):
    _name = 'sale.cost.labor'
    _description = 'Mano de Obra'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Secuencia', default=10)
    sale_line_id = fields.Many2one('sale.order.line', string='Línea de Venta', required=True, ondelete='cascade')
    name = fields.Char(string='Tarea', required=True)
    description = fields.Text(string='Descripción')
    hours = fields.Float(string='Horas', default=1.0)
    user_id = fields.Many2one('res.users', string='Asignado a')
    project_task_id = fields.Many2one('project.task', string='Tarea Proyecto', readonly=True)
    notes = fields.Text(string='Notas')
