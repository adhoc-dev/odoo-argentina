from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_location = fields.Char(string="Ubicacion", copy=False)
