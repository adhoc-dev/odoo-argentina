from odoo import models, fields


class UomUom(models.Model):
    _inherit = 'uom.uom'

    # for compatibility with odumbo till we migrate everything to v13
    # TODO remove on v14 (or before)
    afip_code = fields.Char(related='l10n_ar_afip_code')
