from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    x_studio_field_f6gNw = fields.Date(string="MLS Alta", copy=False)
    x_studio_field_oKrjW = fields.Html(string="Respuesta", copy=False)
