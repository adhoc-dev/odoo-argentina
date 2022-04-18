from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_rating = fields.Selection([('excelente', 'Excelente'), ('bueno', 'Bueno'),
                                        ('regular', 'Regular'), ('malo', 'Malo')],
                                        string="Calificación del proveedor")
