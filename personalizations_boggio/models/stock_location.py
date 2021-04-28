from odoo import models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    x_stk_warehouse_id = fields.Many2one(string="Almacen de stock", comodel_name="stock.warehouse", help="Almacen para ubicaciones de stock", on_delete="set null")
    x_nombre_viejo = fields.Char(string="Nombre Viejo")
    x_orden = fields.Integer(string="Orden")
    x_immediately_usable_qty = fields.Float(string="Disponible para reservar", compute="_compute_x_immediately_usable_qty", help="Stock-entrante", readonly=True, copy=False)

    def _compute_x_immediately_usable_qty(self):
        for record in self:
            record['x_immediately_usable_qty'] = record.qty_available-record.outgoing_qty
