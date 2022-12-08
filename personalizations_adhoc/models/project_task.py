from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    adhoc_product_id = fields.Many2one(
        'adhoc.product', compute='_compute_adhoc_product', store=True, readonly=False,
        domain=[('parent_id', '!=', False)])
    ticket_ids = fields.One2many('helpdesk.ticket', 'task_id')

    @api.depends('adhoc_module_id.adhoc_product_id')
    def _compute_adhoc_product(self):
        for rec in self.filtered('adhoc_module_id.adhoc_product_id'):
            rec.adhoc_product_id = rec.adhoc_module_id.adhoc_product_id
