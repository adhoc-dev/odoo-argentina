##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    # lo moví a product supplier search
    # main_supplier_id = fields.Many2one(
    #     related='seller_ids.name', string="Supplier", store=True,)
    supplier_code = fields.Char(
        related='seller_ids.product_code',
        string="Supplier Code",
        readonly=False,
    )

    location_1 = fields.Char()

    location_2 = fields.Char()

    quantity_per_pack = fields.Char()

    next_deactivate = fields.Date(
    )
