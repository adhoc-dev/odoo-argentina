from odoo import models, fields


class XProductEditorial(models.Model):
    _name = 'x_product_editorial'
    _description = 'product_editorial'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
