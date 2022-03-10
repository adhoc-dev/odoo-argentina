##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class AccountPaymentGroup(models.Model):

    _inherit = 'account.payment.group'

    def write(self, vals):
        if 'state' in vals and vals.get('state') == 'draft':
            for rec in self.mapped('payment_ids').filtered('payment_transaction_id'):
                rec.write({'payment_transaction_id': False})
        return super().write(vals)
