from odoo import models, fields


class productCoil(models.Model):
    _name = 'product.template.coil'
    _description = 'coils'

    name = fields.Char(string="Nombre")
    img = fields.Binary(string="Imagen adjunta")
