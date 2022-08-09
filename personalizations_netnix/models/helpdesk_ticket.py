from datetime import datetime
from odoo import models

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _cron_archive_tickets(self):
        self.env['helpdesk.ticket'].search([
            ('stage_id', '=', 36),
            ('kanban_state', '=', 'done'),
            ('date_last_stage_update', '<', datetime.now().replace(day=1, hour=0, minute=0, second=0))
            ]).write({'active': False})
