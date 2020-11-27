from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_product_id = fields.Many2one(string="Producto", comodel_name="product.product", on_delete="restrict")
