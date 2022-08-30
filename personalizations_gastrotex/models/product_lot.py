from odoo import models, api

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.onchange('expiration_date')
    def _onchange_expiration_date(self):
        self.removal_date = self.expiration_date
