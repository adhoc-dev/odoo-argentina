from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_isbn_order_line = fields.Char(string="ISBN", related="product_id.x_studio_field_5G9jj", copy=False)
