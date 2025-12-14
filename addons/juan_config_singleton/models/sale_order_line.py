from odoo import models, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.constrains('discount')
    def _check_discount_limit(self):
        """Valida que el descuento no exceda el máximo configurado"""
        config = self.env['juan.config.global'].get_config()
        
        # Solo validar si está activado el bloqueo
        if not config.bloquear_exceso:
            return
        
        for line in self:
            if line.discount > config.descuento_maximo:
                raise ValidationError(
                    f'El descuento de {line.discount:.2f}% excede el máximo permitido '
                    f'de {config.descuento_maximo:.2f}%.\n\n'
                    f'Producto: {line.product_id.name}\n'
                    f'Para cambiar el límite, ve a: Mi Configuración → Configuración de Descuentos'
                )
