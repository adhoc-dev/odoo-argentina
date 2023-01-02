from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    # TODO tal vez mover esto de los vinculos a productos tambien a saas_provider_adhoc?
    adhoc_product_id = fields.Many2one('adhoc.product', domain=[('parent_id', '!=', False)])
    task_id = fields.Many2one(comodel_name='project.task')

    def create_linked_task(self):
        for rec in self:
            new_task = rec.task_id.create({
                'name': rec.name,
                'project_id': rec.project_id.id,
                'partner_id': rec.partner_id.id,
                'adhoc_product_id': rec.adhoc_product_id.id,
                'task_description': rec.description,
                'description': rec.ticket_description,
                'user_ids': [(4, rec.project_id.user_id.id, 0)] if rec.project_id.user_id else False,
                'ticket_ids': [(4, rec.id, 0)]
            })
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'helpdesk.ticket'),
                ('res_id', '=', rec.id),
            ])
            for att in attachments:
                att.copy({'res_model': new_task._name, 'res_id': new_task.id})

    @api.model_create_multi
    def create(self, list_value):
        tickets = super().create(list_value)
        if len(tickets) == 1 and list_value and list_value[0].get('task_id'):
            new_ticket = tickets[:1]
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'project.task'),
                ('res_id', '=', list_value[0]['task_id']),
            ])
            for att in attachments:
                att.copy({'res_model': new_ticket._name, 'res_id': new_ticket.id})
        return tickets
