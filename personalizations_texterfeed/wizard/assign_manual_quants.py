from odoo import models, api

class AssignManualQuants(models.TransientModel):
    _inherit = "assign.manual.quants"

    @api.model
    def _prepare_wizard_line(self, move, quant):
        line = super()._prepare_wizard_line(move, quant)
        line["life_date"] = quant.lot_id.life_date
        return line
