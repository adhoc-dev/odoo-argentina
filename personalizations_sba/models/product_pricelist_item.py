from odoo import models, fields


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    x_studio_field_uHw31 = fields.Char(string="ISBN", related="product_tmpl_id.barcode", help="Número de artículo internacional usado para la identificación de producto.", copy=False, store=True)
