from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_salesperson = fields.Boolean(string='Es comercial')
