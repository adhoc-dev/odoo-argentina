from datetime import timedelta

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    adhoc_product_id = fields.Many2one(
        'adhoc.product', compute='_compute_adhoc_product', store=True, readonly=False,
        domain=[('parent_id', '!=', False)])
    ticket_ids = fields.One2many('helpdesk.ticket', 'task_id')
    planned_date_end = fields.Datetime(compute="_compute_planned_date_end", store=True, readonly=False)
    sistemas_planned_hours = fields.Float("Planned Development Hours", help='Time planned for the entire code development')
    planned_hours = fields.Float(compute='_compute_planned_hours', store=True, readonly=False)
    sistemas_planned_lines = fields.Integer("Planned Development Lines")
    technical_team_id = fields.Many2one(related="adhoc_product_id.technical_team_id", store=True)

    def name_get(self):
        result = []
        for task in self:
            result.append((task.id, "%s (#%d)" % (task.name, task._origin.id)))
        return result

    @api.depends('adhoc_module_id.adhoc_product_id')
    def _compute_adhoc_product(self):
        for rec in self.filtered('adhoc_module_id.adhoc_product_id'):
            rec.adhoc_product_id = rec.adhoc_module_id.adhoc_product_id

    @api.onchange('planned_hours', 'planned_date_begin')
    def _compute_planned_date_end(self):
        for rec in self:
            weeks = round(self.sistemas_planned_hours / 5) + 1
            if rec.planned_date_begin:
                rec.planned_date_end = rec.planned_date_begin + timedelta(weeks=weeks)
            else:
                rec.planned_date_end = False

    @api.depends('sistemas_planned_hours')
    def _compute_planned_hours(self):
        for rec in self:
            rec.planned_hours = rec.sistemas_planned_hours * 1.5

    @api.model_create_multi
    def create(self, vals_list):
        # Make customers follower. We need to do this since the customers are no followers of the projects.
        tasks = super().create(vals_list)
        for task in tasks:
            if task.partner_id and task.project_id.privacy_visibility == 'portal':
                task.message_subscribe(partner_ids=task.partner_id.ids)
        return tasks
