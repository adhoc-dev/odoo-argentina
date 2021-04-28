from odoo import models, fields


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    x_num_products = fields.Integer(string="Numero de productos", help="Numero de productos en la categoria")
    x_ventas = fields.Float(string="Ventas aprox de la categoria", readonly=True, copy=False)
    x_google_product_category = fields.Integer(string="google_product_category")
