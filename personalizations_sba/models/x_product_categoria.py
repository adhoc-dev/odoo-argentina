from odoo import models, fields


class XProductCategoria(models.Model):
    _name = 'x_product_categoria'
    _description = 'product_categoria'

    x_name = fields.Char(string="Name", copy=False)
