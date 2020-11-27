from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    x_presupuestado = fields.Boolean(string="Presupuestado")
