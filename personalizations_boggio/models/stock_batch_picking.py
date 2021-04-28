from odoo import models, fields


class StockBatchPicking(models.Model):
    _inherit = 'stock.batch.picking'

    x_fecha_remito = fields.Date(string="Fecha del remito", help="Fecha en la cual confecciono el remito el proveedor.")
    x_fecha_ingreso = fields.Date(string="Fecha de ingreso a boggio", help="Fecha en la cual ingresa la mercadería a la empresa, pero que todavía no fue cargada en el sistema operativo.")
