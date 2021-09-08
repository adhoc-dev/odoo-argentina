##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    supplier_code = fields.Char(
        related='product_id.product_tmpl_id.supplier_code',
    )

    internal_code = fields.Char(
        related='product_id.internal_code',
    )

    product_brand_id = fields.Many2one(
        related='product_id.product_tmpl_id.product_brand_id',
    )
