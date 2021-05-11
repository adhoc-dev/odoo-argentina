from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_keep_remaining = fields.Boolean(string="Mantener Remanente", help="Mantener remanente en esta orden", copy=False)
