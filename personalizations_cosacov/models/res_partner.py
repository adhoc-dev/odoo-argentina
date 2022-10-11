from odoo import api, models, fields
class Partner(models.Model):
    _inherit = 'res.partner'

    product_pricelist_state = fields.Many2one(related='state_id.product_pricelist')
