# -*- coding: utf-8 -*-
import base64
import os
from odoo import fields, models, api


class CR7CelebrationWizard(models.TransientModel):
    _name = 'cr7.celebration.wizard'
    _description = 'CR7 SIUUUU Celebration'

    order_name = fields.Char(string='Pedido', readonly=True)
    message = fields.Text(string='Mensaje', readonly=True)
    cr7_image = fields.Binary(string='CR7', compute='_compute_cr7_image')

    @api.depends('order_name')
    def _compute_cr7_image(self):
        """Cargar imagen de CR7 desde el módulo"""
        for wizard in self:
            # Intentar con CR7.jpg primero, luego otras variantes
            for filename in ['CR7.jpg', 'cr7_siuuu.jpg', 'cr7_siuuu.gif', 'cr7_siuuu.png']:
                img_path = os.path.join(
                    os.path.dirname(__file__), 
                    '..', 'static', 'src', 'img', filename
                )
                if os.path.exists(img_path):
                    try:
                        with open(img_path, 'rb') as f:
                            wizard.cr7_image = base64.b64encode(f.read())
                            return
                    except:
                        pass
            wizard.cr7_image = False
