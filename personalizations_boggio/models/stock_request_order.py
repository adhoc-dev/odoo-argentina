from odoo import models, fields


class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    x_rotacion = fields.Float(string="ROTACION IR", copy=False)
    x_rotacion_local = fields.Float(string="ROTACION IR LOCAL", copy=False)
