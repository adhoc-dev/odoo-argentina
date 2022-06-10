from odoo import api, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.constrains('location_id', 'location_dest_id')
    def _check_external_location(self):
        external_moves = self.filtered(lambda x: x.location_id.external_stock_source or x.location_dest_id.external_stock_source)
        if external_moves:
            raise UserError("No se puede crear un stock move con una ubicación externa. Revisar las ubicaciones de origen y destino, el campo 'External Stock Source' debe estar deshabilitado.")
