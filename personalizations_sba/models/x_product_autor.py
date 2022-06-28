from odoo import models, fields


class XProductAutor(models.Model):
    _name = 'x_product_autor'
    _description = 'product_autor'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
