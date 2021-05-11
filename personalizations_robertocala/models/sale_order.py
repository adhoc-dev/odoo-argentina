from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_keep_remaining = fields.Boolean(string="Mantener el Remanente", help="Mantener el Remanente en esta orden", copy=False)
