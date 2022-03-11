from odoo import models, fields

class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    date_start = fields.Date(required=True)
    purchase_type = fields.Selection([('bajo','Bajo'),('medio','Medio'), ('alto','Alto')])
