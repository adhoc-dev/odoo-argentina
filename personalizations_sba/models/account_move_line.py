from odoo import models, fields


class AccountMoveLLine(models.Model):
    _inherit = 'account.move.line'

    x_isbn = fields.Char(string="ISBN", related="product_id.x_studio_field_5G9jj", copy=False)
