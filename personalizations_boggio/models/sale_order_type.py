from odoo import models, fields


class SaleOrderType(models.Model):
    _inherit = 'sale.order.type'

    x_express = fields.Boolean(string="Express", help="Indica si el circuito es express o mostrador", copy=False)
    x_activo = fields.Boolean(string="x_activo", copy=False)
    x_paralelo = fields.Boolean(string="x_paralelo", help="Circuito paralelo", copy=False)
