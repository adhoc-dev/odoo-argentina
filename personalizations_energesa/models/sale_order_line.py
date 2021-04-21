from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_sale_orde_team_id = fields.Many2one(string="Canal de ventas", related="order_id.team_id", on_delete="set null", readonly=True, copy=False, store=True)
