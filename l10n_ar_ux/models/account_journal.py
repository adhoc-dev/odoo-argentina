##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api, _


class AccountJournal(models.Model):

    _inherit = 'account.journal'

    l10n_ar_document_type_ids = fields.Many2many('l10n_latam.document.type', string='Document Types')
    qr_code_label = fields.Char(
        string="QR Code Label",
        help="String to display before the QR Code on the invoice report."
    )
    qr_code = fields.Char(
        string="QR Code",
        help="String to generate the QR Code that will be displayed on the invoice report."
    )
    l10n_ar_is_pos = fields.Boolean(compute="_compute_l10n_ar_is_pos", store=True, readonly=False, string="Is AFIP POS?")

    @api.depends('l10n_latam_country_code', 'type', 'l10n_latam_use_documents')
    def _compute_l10n_ar_is_pos(self):
        ar_sale_use_documents = self.filtered(
            lambda x: x.l10n_latam_country_code == 'AR' and x.type == 'sale' and x.l10n_latam_use_documents)
        ar_sale_use_documents.l10n_ar_is_pos = True
        (self - ar_sale_use_documents).l10n_ar_is_pos = False

    def _l10n_ar_create_document_sequences(self):
        """ IF AFIP Configuration change try to review if this can be done and then create / update the document
        sequences """
        self.ensure_one()

        if self.company_id.country_id == self.env.ref('base.ar') and self.l10n_latam_use_documents and self.type == 'purchase':
            # TODO KZ improve, create purchase manually using document types
            return False

        return super()._l10n_ar_create_document_sequences()
