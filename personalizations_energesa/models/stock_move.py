from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    x_standard_price = fields.Float(string="Costo Contable", compute="_compute_x_standard_price", readonly=True, copy=False, store=True)

    @api.depends('__last_update')
    def _compute_x_standard_price(self):
        for rec in self:
          rec['x_standard_price'] = rec.product_id.standard_price
