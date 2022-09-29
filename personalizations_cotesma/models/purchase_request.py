from odoo import models, fields

class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    description = fields.Text(required=True)
    priority = fields.Selection([('0', 'Normal'),('1', 'Urgente')], string="Prioridad")
