from odoo import models, fields


class XProductVersion(models.Model):
    _name = 'x_product_version'
    _description = 'product_version'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
