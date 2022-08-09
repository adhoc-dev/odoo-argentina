from datetime import datetime
from odoo import models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _cron_archive_tasks(self):
        self.env['project.task'].search([
            ('stage_id', '=', 8),
            ('kanban_state', '=', 'done'),
            ('date_last_stage_update', '<', datetime.now().replace(day=1, hour=0, minute=0, second=0))
            ]).write({'active': False})
