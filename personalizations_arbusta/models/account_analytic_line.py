from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    x_studio_field_yC90r = fields.Integer(string="TCs. Avisos. Registros", copy=False)
