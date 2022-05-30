from numpy import product
from odoo import models, fields


class PriceHistory(models.Model):
    _name = 'price.history'
    _description = 'price.history'

    product_template_id = fields.Many2one('product.template')
    list_price = fields.Float("Precio de venta")
    standard_price = fields.Float("Precio de coste")
