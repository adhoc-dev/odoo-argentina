from odoo import models, fields


class HelpdeskTag(models.Model):
    _inherit = 'helpdesk.tag'

    x_studio_field_lLRzd = fields.Many2one(string="Equipo de Soporte", comodel_name="helpdesk.team",
                                           on_delete="set null", copy=False)
