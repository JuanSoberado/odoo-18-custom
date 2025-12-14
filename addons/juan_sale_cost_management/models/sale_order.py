# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Crear tareas en proyecto desde la mano de obra definida"""
        res = super().action_confirm()
        for order in self:
            for line in order.order_line:
                if line.labor_ids and line.task_id:
                    for labor in line.labor_ids:
                        if not labor.project_task_id:
                            task_vals = {
                                'name': f"{labor.name} - {line.product_id.name}",
                                'project_id': line.task_id.project_id.id,
                                'user_ids': [(4, labor.user_id.id)] if labor.user_id else [],
                                'description': labor.description or '',
                                'planned_hours': labor.hours,
                                'sale_line_id': line.id,
                            }
                            task = self.env['project.task'].create(task_vals)
                            labor.project_task_id = task.id
        return res
