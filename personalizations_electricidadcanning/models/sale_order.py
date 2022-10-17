from odoo import models, fields


class sale_order(models.Model):
    _inherit = 'sale.order'

    x_discount_hide = fields.Boolean(default=False)
