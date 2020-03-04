##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, fields


class AccountChartTemplate(models.Model):

    _inherit = 'account.chart.template'

    # TODO we should move this to another module because not only argentina use this
    # or use account_opening_move_id?
    opening_clousure_account_id = fields.Many2one(
        'account.account.template',
        string='Opening / Closure Account',
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)],
    )

    def _load(self, sale_tax_rate, purchase_tax_rate, company):
        """ Set non monetary tag when installing chart of account """
        res = super()._load(sale_tax_rate, purchase_tax_rate, company)
        self.env['account.account'].set_non_monetary_tag(company)
        return res

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        """ Add more journals commonly used in argentina localization """
        journal_data = super()._prepare_all_journals(acc_template_ref, company, journals_dict)

        opening_clousure_account_id = acc_template_ref.get(self.opening_clousure_account_id.id)
        journals = [
            # TODO change to english
            (_('Liquidación de Impuestos'), 'LIMP', 'general', False),
            (_('Sueldos y Jornales'), 'SYJ', 'general', False),
            (_('Asientos de Apertura / Cierre'), 'A/C', 'general', opening_clousure_account_id),
        ]
        for name, code, journal_type, default_account_id in journals:
            journal_data.append({
                'type': journal_type,
                'name': name,
                'code': code,
                'default_credit_account_id': default_account_id,
                'default_debit_account_id': default_account_id,
                'company_id': company.id,
                'show_on_dashboard': False,
                'update_posted': True,
            })
        return journal_data

    def _create_bank_journals(self, company, acc_template_ref):
        """ We create the withholding journal if withholding module installed """
        if company.country_id == self.env.ref('base.ar'):
            return super(AccountChartTemplate, self.with_context(create_withholding_journal=True))._create_bank_journals(
                company, acc_template_ref)
        return super()._create_bank_journals(company, acc_template_ref)
