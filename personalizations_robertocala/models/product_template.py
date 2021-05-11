from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_operation_type = fields.Selection(string="Tipo de Operacion", selection=[('distribuidora', 'Distribuidora'),('roberto_cala', 'Roberto Cala'),('50-50','50-50')]																	)
    x_other_sale_description = fields.Char(string="Other Sale Description")
    x_studio_field_4YsN7 = fields.Char(string="Categoria Publica", related="public_categ_ids.name", readonly=True, translate=True, copy=False)
