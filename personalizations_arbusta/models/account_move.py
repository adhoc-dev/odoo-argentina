from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_studio_field_PZO8w = fields.Boolean(string="OK Operaciones", tracking=100, copy=False)
