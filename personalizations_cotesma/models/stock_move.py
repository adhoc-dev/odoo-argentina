from requests import request
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _assign_picking(self):
        res = super()._assign_picking()
        for move in self.filtered(lambda s: s.picking_id):
            request_order_id = False
            if move.stock_request_ids:
                request_order_id = move.stock_request_ids.mapped('order_id')[0]
            elif move.move_dest_ids and move.move_dest_ids.filtered('stock_request_ids'):
                request_order_id = move.move_dest_ids.filtered('stock_request_ids').mapped('stock_request_ids.order_id')[0]
            if request_order_id and not move.picking_id.observations:
                move.picking_id.observations = request_order_id.observations
        return res
