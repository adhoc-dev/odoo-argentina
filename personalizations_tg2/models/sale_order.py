from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_amt_to_invoice = fields.Monetary(string="Monto a facturar", compute="_compute_x_amt_to_invoice", copy=False, store=True)
    x_closed = fields.Boolean(string="Cerrado")

    @api.depends('order_line','order_line.untaxed_amount_to_invoice')
    def _compute_x_amt_to_invoice(self):
        for sale in self:
            sale.x_amt_to_invoice = sum(sale.order_line.mapped('untaxed_amount_to_invoice'))

    def change_order_state(self):
        for rec in self:
            rec.x_closed = False if rec.x_closed else True

