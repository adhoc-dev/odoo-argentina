from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_date_change_stage = fields.Date(string="Fecha de cambio de etapa	")
