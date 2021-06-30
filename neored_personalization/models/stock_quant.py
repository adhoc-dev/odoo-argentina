from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # TODO remove in v15
    lot_id = fields.Many2one(check_company=False)
