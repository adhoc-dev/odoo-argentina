from odoo import models, fields


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    x_studio_field_uHw31 = fields.Char(string="New Campo relacionado", related="product_tmpl_id.barcode", help="Número de artículo internacional usado para la identificación de producto.", readonly=True, copy=False, store=True)
