from odoo import models, api


class AccountFollowupReport(models.AbstractModel):
    _inherit = 'account.followup.report'

    @api.model
    def send_email(self, options):
        self = self.with_context(claims_partner=True)
        return super().send_email(options)


    @api.multi
    def get_html(self, options, line_id=None, additional_context=None):
        self = self.with_context(claims_partner=True)
        return super().get_html(options, line_id=line_id, additional_context=additional_context)
