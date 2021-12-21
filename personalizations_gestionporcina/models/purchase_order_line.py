from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    observations = fields.Text(string="Observaciones", copy=False)
