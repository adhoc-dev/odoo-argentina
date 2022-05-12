from odoo import api, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _query_get(self, domain=None):
        if 'debt_balance_company_ids' in self.env.context:
            return super(AccountMoveLine, self.with_context(company_id=False, company_ids=self.env.context.get('debt_balance_company_ids')))._query_get(domain)
        return super()._query_get(domain)
