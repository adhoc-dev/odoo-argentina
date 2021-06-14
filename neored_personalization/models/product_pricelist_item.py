##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    _order = "applied_on, min_quantity desc, brand_id, manufacturer, categ_id desc, id desc"

    brand_id = fields.Many2one('product.brand', string="Marca")
    manufacturer = fields.Many2one('res.partner', string="Fabricante")
