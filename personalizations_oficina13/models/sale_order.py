from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    approve_picking = fields.Boolean(string="Venta en cuenta corriente", required=False, track_visibility="always", copy=False)
