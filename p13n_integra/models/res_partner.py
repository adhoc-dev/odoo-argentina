from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    dv = fields.Integer()

    @api.constrains('dv')
    def _check_field_dv(self):
        if self.dv < 0  or self.dv > 99:
            raise ValidationError(_('Ingresa un valor entre 0 y 99'))
