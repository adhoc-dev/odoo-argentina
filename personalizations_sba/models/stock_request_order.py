from odoo import models, fields


class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    x_studio_field_DCi1j = fields.Text(string="Destinatario", copy=False)
