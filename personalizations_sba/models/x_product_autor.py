from odoo import models, fields


class XProductAutor(models.Model):
    _name = 'x_product_autor'
    _description = 'product_autor'

    x_name = fields.Char(string="Name", copy=False)
