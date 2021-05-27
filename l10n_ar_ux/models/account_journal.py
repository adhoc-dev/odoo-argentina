# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class AccountJournal(models.Model):

    _inherit = "account.journal"

    l10n_latam_document_type_ids = fields.Many2many(
        'l10n_latam.document.type', 'jorunal_document_type_rel',
        'journal_id', 'document_type_id', string='Document Types'
    )

    def _get_l10n_ar_afip_pos_types_selection(self):
        """ Add a new options to the selection field AFIP POS System """
        res = super()._get_l10n_ar_afip_pos_types_selection()
        res.append(('NOT_APPLY', _('Do not Correspond / Not Apply')))
        return res
