from odoo import fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    product_id = fields.Many2one(comodel_name='product.product', string='Productos')
    uen_id = fields.Many2one(comodel_name='crm.strategic_business_unit', string='U.E.N.')
    location_id = fields.Many2one(comodel_name='crm.location', string='Lugar')
