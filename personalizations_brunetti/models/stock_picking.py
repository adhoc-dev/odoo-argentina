from odoo import models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        if self.picking_type_code == "outgoing" and self.move_ids_without_package.filtered(lambda x: not x.analytic_tag_ids):
            raise UserError("Cada linea de la transferencia debe tener al menos una etiqueta analitica")
        return res
