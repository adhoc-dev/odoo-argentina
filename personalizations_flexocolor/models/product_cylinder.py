from odoo import models, fields


class productCylinder(models.Model):
    _name = 'product.template.cylinder'
    _description = 'types of cylinders'

    name = fields.Char(string="Cilindro")
