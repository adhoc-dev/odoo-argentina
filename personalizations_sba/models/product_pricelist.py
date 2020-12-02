from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    x_porcentaje_cargo_extra = fields.Float(string="Porcentaje de recargo por mora", copy=False)
