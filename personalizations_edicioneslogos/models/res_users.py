from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    x_comercial_logos = fields.Boolean(string="Comercial logos", help="Este campo identifica el comercial que va a usar en la Orden de venta")
