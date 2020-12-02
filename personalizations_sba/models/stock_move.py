from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    x_studio_field_yBQWe = fields.Char(string="ISBN", related="product_id.x_studio_field_5G9jj", readonly=True, copy=False, store=True)
