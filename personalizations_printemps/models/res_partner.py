from odoo import api, models, fields, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    debt_balance = fields.Monetary(
        compute='_compute_debt_balance',
        currency_field='currency_id',
    )

    @api.depends('credit','debit')
    @api.depends_context('companies')
    def _compute_debt_balance(self):
        for rec in self.with_context(debt_balance_company_ids=self.env.companies.ids):
            rec.debt_balance = rec.credit - rec.debit
