from odoo import models, fields


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    x_razon_devolucion = fields.Many2one(string="Razon de la devolucion", comodel_name="x_devolucion_tags.devolucion_tags", on_delete="set null")

    def _create_returns(self):
        # add to new picking for return the reason tag
        new_picking, pick_type_id = super()._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        picking.write({'x_razon_devolucion': self.x_razon_devolucion})
        return new_picking, pick_type_id
