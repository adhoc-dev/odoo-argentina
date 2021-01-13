# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'

    barcode = fields.Char(string='Barcode', readonly=True)
    author_id = fields.Many2one('product.attribute.value', string='Author', readonly=True)
    editorial_id = fields.Many2one('product.attribute.value', string='Editorial', readonly=True)
    collection_id = fields.Many2one('product.attribute.value', string='Collecion', readonly=True)
    state_id = fields.Many2one('res.country.state', string='State', readonly=True)
    city = fields.Char(string='City', readonly=True)

    def _select(self):
        return super()._select() + """,
            product.barcode as barcode,
            template.author_id as author_id,
            template.editorial_id as editorial_id,
            template.collection_id as collection_id,
            partner.state_id as state_id,
            partner.city as city
            """

    def _group_by(self):
        return super()._group_by() + ", product.barcode, template.author_id, template.editorial_id, template.collection_id, partner.state_id, partner.city"
