from odoo import models, fields


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    x_origen = fields.Many2one(string="Origen de inventario", comodel_name="x_origen_tags", help="En que capa surgió el problema de inventario? (cliente, interno, auditoria o proveedor)")
