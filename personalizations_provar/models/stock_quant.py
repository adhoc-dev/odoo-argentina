from odoo import fields, models, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    lot_name = fields.Char(string='Lot Name')
