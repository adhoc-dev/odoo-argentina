from odoo import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    x_budget_line_ids = fields.One2many(string="Líneas de Presupuesto", comodel_name="account.analytic.line", inverse_name="account_id", domain=[('x_presupuestado', '=', True)])
