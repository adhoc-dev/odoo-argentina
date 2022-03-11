from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_user_id = fields.Many2one('res.users', domain="[('is_salesperson', '=', True)]")
