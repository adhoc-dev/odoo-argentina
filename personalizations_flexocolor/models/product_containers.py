from odoo import models, fields


class productContainers(models.Model):
    _name = 'product.template.containers'
    _description = 'types of containers'

    name = fields.Char(string="Envase")
