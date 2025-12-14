from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ConfigGlobal(models.Model):
    _name = 'juan.config.global'
    _description = 'Configuración de Control de Descuentos'
    
    # CLAVE: Esta línea hace que sea un SINGLETON
    _rec_name = 'display_name'
    
    display_name = fields.Char(
        string='Nombre',
        default='Configuración de Descuentos',
        readonly=True
    )
    
    descuento_maximo = fields.Float(
        string='Descuento Máximo Permitido (%)',
        default=15.0,
        required=True,
        help='Descuento máximo que pueden aplicar los vendedores en líneas de pedido. '
             'Si un vendedor intenta poner un descuento mayor, el sistema lo impedirá.'
    )
    
    email_notificacion = fields.Char(
        string='Email de Notificación',
        required=True,
        help='Email al que se enviarán notificaciones cuando se superen los límites'
    )
    
    bloquear_exceso = fields.Boolean(
        string='Bloquear Descuentos Excesivos',
        default=True,
        help='Si está activado, impide guardar líneas con descuentos superiores al máximo. '
             'Si está desactivado, solo muestra una advertencia.'
    )
    
    descuento_minimo_alerta = fields.Float(
        string='Descuento Mínimo para Alerta (%)',
        default=10.0,
        help='A partir de este descuento se muestra una advertencia visual en la línea'
    )
    
    # Constraint para asegurar que solo haya UN registro
    @api.constrains('descuento_maximo')
    def _check_singleton(self):
        if self.search_count([]) > 1:
            raise ValidationError(
                'Solo puede existir un registro de configuración global. '
                'Este es un modelo singleton.'
            )
    
    # Método helper para obtener siempre el único registro
    @api.model
    def get_config(self):
        """Obtiene o crea la configuración global (singleton)"""
        config = self.search([], limit=1)
        if not config:
            config = self.create({
                'descuento_maximo': 15.0,
            })
        return config
