from odoo import fields, models

class CountryState(models.Model):
    _inherit = 'res.country.state'

    product_pricelist = fields.Many2one('product.pricelist', string="Tarifa")

