from odoo import models, fields


class XProductSubcategoria(models.Model):
    _name = 'x_product_subcategoria'
    _description = 'product_subcategoria'

    x_name = fields.Char(string="Name", copy=False)
