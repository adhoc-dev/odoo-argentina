from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_amt_to_invoice = fields.Monetary(string="Monto a facturar", compute="_compute_x_amt_to_invoice", readonly=True, copy=False, store=True)
    x_closed = fields.Boolean(string="Cerrado")

    @api.depends('order_line','order_line.amt_to_invoice')
    def _compute_x_amt_to_invoice(self):
        for sale in self:
              
            sale['x_amt_to_invoice'] = sum(sale.order_line.mapped('amt_to_invoice'))
