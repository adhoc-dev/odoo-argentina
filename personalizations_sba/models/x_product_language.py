from odoo import models, fields


class XProductLanguage(models.Model):
    _name = 'x_product_language'
    _description = 'product_language'

    x_name = fields.Char(string="Name", copy=False)
