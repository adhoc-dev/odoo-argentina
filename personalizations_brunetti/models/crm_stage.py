from odoo import models, fields


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    x_automation_stages = fields.Boolean(string="Cambio de etapa Automatico")
    x_days_to_chages = fields.Integer(string="Dias de cambio de etapa", help="Introduzca la cantidad de días que debe permanecer en esta etapa una iniciativa. ")
    x_to_stage_id = fields.Many2one(string="Etapa a cambiar", comodel_name="crm.stage")
