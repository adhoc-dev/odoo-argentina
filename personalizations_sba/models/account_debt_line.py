from odoo import models, fields


class AccountDebtLine(models.Model):
    _inherit = 'account.debt.line'

    x_x_state_invoice = fields.Selection(string="Estado de vencimiento de factura", related="invoice_id.x_state_invoice", readonly=True, copy=False)
