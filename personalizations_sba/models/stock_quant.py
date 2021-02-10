from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    x_studio_field_2oKwz = fields.Char(string="ISBN", related="product_id.x_studio_field_5G9jj", copy=False, store=True)
