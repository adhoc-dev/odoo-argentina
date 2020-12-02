from odoo import models, fields


class XProductFamilia(models.Model):
    _name = 'x_product_familia'
    _description = 'product_familia'

    x_name = fields.Char(string="Name", copy=False)
