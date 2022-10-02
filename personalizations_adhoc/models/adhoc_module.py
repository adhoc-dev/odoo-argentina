from odoo import models, fields


class AdhocModule(models.Model):
    _inherit = 'adhoc.module'

    adhoc_product_id = fields.Many2one('adhoc.product')
