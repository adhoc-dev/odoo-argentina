from odoo import models


class ResCompanyInterest(models.Model):
    _inherit = 'res.company.interest'

    def _prepare_interest_invoice(self, partner, debt, to_date, journal):
        res = super()._prepare_interest_invoice(partner, debt, to_date, journal)
        res.update({
            'student_id': partner.id,
            'partner_id': partner.parent_id.id,
        })
        return res

    def create_invoices(self, to_date, groupby='student_id'):
        return super().create_invoices(to_date, groupby=groupby)
