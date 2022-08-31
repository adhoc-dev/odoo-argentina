from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        if self.env.user.has_group('purchase.group_purchase_manager') and not self.env.user.has_group('account.group_account_invoice'):
            return super(AccountMove, self.sudo())._post(soft)
        return super()._post(soft)
