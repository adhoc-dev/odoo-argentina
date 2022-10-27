from odoo import models, fields


class AdhocModuleModule(models.Model):
    _inherit = 'adhoc.module.module'

    adhoc_product_id = fields.Many2one(related='module_id.adhoc_product_id', store=True)
