from odoo import fields, models


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    product_class = fields.Many2one('product.class', related='product_tmpl_id.product_class', store=True, string='Clase de artículo')
    product_maker = fields.Many2one('product.maker', related='product_tmpl_id.product_maker', store=True, string='Fabricante')
    product_brand = fields.Many2one('product.vehicle.brand', related='product_tmpl_id.product_brand', store=True, string='Marca de vehículo')
    product_model = fields.Many2one('product.vehicle.model', related='product_tmpl_id.product_model', store=True, string='Modelo de vehículo')
