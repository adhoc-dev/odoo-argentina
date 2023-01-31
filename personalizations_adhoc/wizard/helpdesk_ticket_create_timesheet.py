from odoo import models


class HelpdeskTicketCreateTimesheet(models.TransientModel):
    _inherit = 'helpdesk.ticket.create.timesheet'

    def action_generate_timesheet(self):
        super(HelpdeskTicketCreateTimesheet, self.with_context(bypass_constraint=True)).action_generate_timesheet()
