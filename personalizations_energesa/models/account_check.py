from odoo import models, fields


class AccountCheck(models.Model):
    _inherit = 'account.check'

    x_fecha_reperfilada = fields.Date(string="Fecha Reperfilada", copy=False)
