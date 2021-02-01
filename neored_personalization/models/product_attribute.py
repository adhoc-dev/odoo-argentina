from odoo import models, api


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    def write(self, vals):
        """To avoid raising error if we're writing the same vale with odumbo, we pop de value if it's a dummy write"""
        if 'create_variant' in vals and all(x.create_variant == vals.get('create_variant') for x in self):
            vals.pop('create_variant')
        return super().write(vals)
