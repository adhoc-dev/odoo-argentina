from odoo import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    x_isbn = fields.Char(string="ISBN", related="product_id.x_studio_field_5G9jj", readonly=True, copy=False)
