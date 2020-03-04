##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.onchange('type', 'l10n_latam_use_documents', 'l10n_ar_afip_pos_system', 'code')
    def onchange_name(self):
        """ Auto complete the name with the information about the journal type the type of invoice and POS number """
        company = self.company_id or self.env.company
        if self.type == 'sale' and company.country_id == self.env.ref('base.ar') and self.l10n_latam_use_documents:
            suffix = self._get_journal_sale_type().get(self.l10n_ar_afip_pos_system, '')
            self.name = _('Sales') + (' ' + suffix if suffix else '') + (' ' + self.code if self.code else '')

    @api.model
    def _get_journal_sale_type(self):
        return {
            'II_IM': _('Preprinted'),
            'RLI_RLM': _('Online'),
            'BFERCEL': _('Online'),
            'FEERCELP': _('Billing Plus'),
            'FEERCEL': _('Online'),
        }
