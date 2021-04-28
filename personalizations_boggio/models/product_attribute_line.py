from odoo import models, fields


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    x_product_brand_id = fields.Many2one(string="Brand", related="product_tmpl_id.product_brand_id", help="Brand", on_delete="set null", readonly=True, copy=False)
