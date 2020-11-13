from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        res = super()._action_confirm()
        for order in self:
            analytic_accounts = self.env['account.analytic.account']
            for line in order.order_line.filtered('product_id'):
                default_analytic_account = self.env['account.analytic.default'].sudo().account_get(
                    product_id=line.product_id.id,
                    user_id=self.env.uid,
                    date=order.date_order,
                    company_id=order.company_id.id,
                )
                if default_analytic_account.analytic_id:
                    analytic_accounts |= default_analytic_account.analytic_id
            if analytic_accounts:
                order.analytic_account_id = analytic_accounts[0]
        return res
