from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    adhoc_product_id = fields.Many2one('adhoc.product')
    task_id = fields.Many2one(comodel_name='project.task')

    def create_linked_task(self):
        for rec in self:
            rec.task_id.create({
                'name': rec.name,
                'project_id': rec.project_id.id,
                'partner_id': rec.partner_id.id,
                'adhoc_product_id': rec.adhoc_product_id.id,
                'task_description': rec.ticket_description,
                'description': rec.description,
                'ticket_ids': [(4, rec.id, 0)]
            })