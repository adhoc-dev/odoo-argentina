from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    tag_ids = fields.Many2many(required=True)
