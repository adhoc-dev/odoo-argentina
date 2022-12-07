from odoo import models, fields


class AdhocModule(models.Model):
    _inherit = 'adhoc.module'

    adhoc_product_id = fields.Many2one('adhoc.product')
    product_category_id = fields.Many2one('adhoc.product', related='adhoc_product_id.product_category_id', store=True)
