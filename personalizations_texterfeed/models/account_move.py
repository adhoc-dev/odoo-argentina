from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def post(self):
        if self.env.user.has_group('purchase.group_purchase_manager') and not self.env.user.has_group('account.group_account_invoice'):
            return super(AccountMove, self.sudo()).post()
        return super().post()
