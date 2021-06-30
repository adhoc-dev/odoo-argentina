from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # TODO remove in v15
    lot_id = fields.Many2one(check_company=False)
