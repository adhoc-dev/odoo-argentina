from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_isbn_purchase = fields.Char(string="ISBN", related="product_id.x_studio_field_5G9jj", readonly=True, copy=False, store=True)
