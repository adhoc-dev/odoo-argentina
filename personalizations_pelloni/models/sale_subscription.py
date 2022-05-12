from odoo import models, fields, api


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    main_direct_debit_mandate_id = fields.Many2one(
        'account.direct_debit.mandate', compute='_compute_main_direct_debit_mandate', store=True,
        string="Direct Debit Mandate")

    @api.depends('partner_id.commercial_partner_id.direct_debit_mandate_ids.state')
    def _compute_main_direct_debit_mandate(self):
        for rec in self:
            active_mandates = rec.partner_id.commercial_partner_id.direct_debit_mandate_ids.filtered(
                lambda x: x.state == 'active')
            rec.main_direct_debit_mandate_id = active_mandates[0].id if active_mandates else False
