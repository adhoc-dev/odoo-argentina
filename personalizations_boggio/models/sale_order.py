from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_monto_USD = fields.Float(string="Monto Presupuesto en USD", help="Se graba el monto del presupuesto en dolares IVA incluido", readonly=True, copy=False)
    x_info_cc = fields.Char(string="Info CC", readonly=True, copy=False)
