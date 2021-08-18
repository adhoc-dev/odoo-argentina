from odoo import models, fields


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    x_fecha_remito = fields.Date(string="Fecha del remito", help="Fecha en la cual confecciono el remito el proveedor.")
    x_fecha_ingreso = fields.Date(string="Fecha de ingreso a boggio", help="Fecha en la cual ingresa la mercadería a la empresa, pero que todavía no fue cargada en el sistema operativo.")

    def get_data_products(self):
        list_product=[]
        for line in self.mapped('move_line_ids').filtered(lambda s: s.state == 'done'):
            list_product.append((line.product_id, line.qty_done))
        return list_product