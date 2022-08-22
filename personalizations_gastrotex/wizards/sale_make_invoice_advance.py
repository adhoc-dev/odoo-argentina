from odoo import models

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super()._prepare_invoice_values(order, name, amount, so_line)
        if self.advance_payment_method in ['percentage', 'fixed']:
            invoice_vals['is_down_payment'] = True
        return invoice_vals
