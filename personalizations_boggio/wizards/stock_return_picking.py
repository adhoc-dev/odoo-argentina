from odoo import models, fields


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    x_razon_devolucion = fields.Many2one(string="Razon de la devolucion", comodel_name="x_devolucion_tags.devolucion_tags", on_delete="set null")
