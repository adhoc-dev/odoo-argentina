from odoo import models

class AccountInvoicePartialWizard(models.TransientModel):
    _inherit = 'account.invoice.partial.wizard'

    def compute_new_quantity(self):
        self.ensure_one()
        self.invoice_id.is_down_payment = True
        super().compute_new_quantity()
