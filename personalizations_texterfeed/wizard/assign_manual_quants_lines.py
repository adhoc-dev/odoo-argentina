from odoo import models, fields

class AssignManualQuantsLines(models.TransientModel):
    _inherit = "assign.manual.quants.lines"

    life_date = fields.Datetime(string="Fecha de caducidad")
