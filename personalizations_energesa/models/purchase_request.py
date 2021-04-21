from odoo import models, fields


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    x_plantilla = fields.Boolean(string="Es Plantilla", copy=False)
