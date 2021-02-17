from odoo import fields, models


class StockValuationLayer(models.Model):
    """Stock Valuation Layer"""

    _inherit = 'stock.valuation.layer'

    barcode = fields.Char(related="product_id.barcode")
