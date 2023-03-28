from odoo import fields, models


class ProductClass(models.Model):
    _name = 'product.class'
    _description = 'Clase de producto'

    name = fields.Char(string='Name', required=True)


class ProductMaker(models.Model):
    _name = 'product.maker'
    _description = 'Fabricante del producto'

    name = fields.Char(string='Fabricante', required=True)


class ProductBrand(models.Model):
    _name = 'product.vehicle.brand'
    _description = 'Marca de vehículo'

    name = fields.Char(string='Marca de vehículo', required=True)


class ProductModel(models.Model):
    _name = 'product.vehicle.model'
    _description = 'Modelo de vehículo'

    name = fields.Char(string='Modelo de vehículo', required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_class = fields.Many2one('product.class', string='Clase de artículo')
    product_maker = fields.Many2one('product.maker', string='Fabricante')
    product_brand = fields.Many2one('product.vehicle.brand', string='Marca de vehículo')
    product_model = fields.Many2one('product.vehicle.model', string='Modelo de vehículo')
