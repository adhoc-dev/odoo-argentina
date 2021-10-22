from odoo import fields, models


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    cuota_inicial = fields.Integer(string='Cuota inicial', default=1)
