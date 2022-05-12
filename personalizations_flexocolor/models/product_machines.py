from odoo import models, fields


class productContainers(models.Model):
    _name = 'product.template.machines'
    _description = 'machines'

    name = fields.Char(string="Máquina")
    cylinder_ids = fields.Many2many('product.template.cylinder', string="Cilindros")
