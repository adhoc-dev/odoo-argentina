from odoo import models, fields


class ProductAbstract(models.Model):
    _name = 'product.abstract'
    _description = 'product.abstract'

    product_tmpl_ids = fields.One2many(
        'product.template',
        'product_abstract_id',
    )
