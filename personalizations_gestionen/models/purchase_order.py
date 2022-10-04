from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    invoicing_company_id = fields.Many2one('res.company', string="Compañia de Facturacion", required=False)
