from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    x_studio_field_yC90r = fields.Integer(string="TCs. Avisos. Registros", copy=False)
    percentage = fields.Selection(
        string="Porcentaje para horas extras", selection=[("100","100"),("150","150"),("200","200")],default="100")
