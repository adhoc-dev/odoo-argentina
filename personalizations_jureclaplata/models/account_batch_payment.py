from odoo import models


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    def get_partner_identification(self, payment):
        invoice = payment.invoice_ids[0]
        return invoice.student_id.student_code or ''
