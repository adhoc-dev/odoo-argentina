from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_ubica_sfe = fields.Char(string="Ubicacion SFE", related="product_tmpl_id.x_ubica_sfe", help="Ubicacion SFE", readonly=True, copy=False)
    x_ubica_sfe2 = fields.Char(string="Ubicacion SFE2", related="product_tmpl_id.x_ubica_sfe2", help="Ubicacion SFE", readonly=True, copy=False)
    x_ubica_raf = fields.Char(string="Ubicacion RAF", related="product_tmpl_id.x_ubica_raf", help="Ubicacion RAF", readonly=True)
    x_ubica_raf2 = fields.Char(string="Ubicacion RAF2", related="product_tmpl_id.x_ubica_raf2", help="Ubicacion RAF2", readonly=True)
    x_marca = fields.Char(string="Marcas", related="product_tmpl_id.product_brand_id.name", help="Marca (.name)", readonly=True, copy=False)
    x_google_product_category = fields.Integer(string="google_product_category", help="Campo para Google Merchant")
    x_power = fields.Float(string="Potencia en W", help="Potencia en W para reportes")
