from odoo import models, fields


class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = 'project.task.create.timesheet'

    task_commercial_partner_id = fields.Many2one('res.partner', related='task_id.commercial_partner_id')
    task_allow_billable = fields.Boolean(related='task_id.allow_billable')
    task_partner_id = fields.Many2one('res.partner', related='task_id.partner_id')
    so_line = fields.Many2one('sale.order.line', string='Sales Order Item')

    def save_timesheet(self):
        values = {
            'task_id': self.task_id.id,
            'project_id': self.task_id.project_id.id,
            'date': fields.Date.context_today(self),
            'name': self.description,
            'user_id': self.env.uid,
            'unit_amount': self.task_id._get_rounded_hours(self.time_spent * 60),
            'so_line':self.so_line.id
        }
        self.task_id.user_timer_id.unlink()
        return self.env['account.analytic.line'].create(values)
