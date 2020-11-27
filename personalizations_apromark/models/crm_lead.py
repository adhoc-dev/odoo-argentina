from odoo import fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    product_id = fields.Many2one(comodel_name='product.product', string='Productos')
    location_id = fields.Many2one(comodel_name='crm.location', string='Lugar')
