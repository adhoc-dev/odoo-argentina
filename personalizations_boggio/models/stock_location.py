from odoo import models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    x_stk_warehouse_id = fields.Many2one(string="Almacen de stock", comodel_name="stock.warehouse", help="Almacen para ubicaciones de stock", on_delete="set null")
    x_nombre_viejo = fields.Char(string="Nombre Viejo")
    x_orden = fields.Integer(string="Orden")
