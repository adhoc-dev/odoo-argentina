from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    name = fields.Char(string='Orden', copy=False, readonly=True,
                       required=True, default=lambda self: _('New'))
    lugar_de_servicio = fields.Many2one('res.partner', string='Lugar de Servicio', required=True, help="Dirección donde se prestará el servicio.")
    partner_email = fields.Char(related='partner_id.email', string="Email", readonly=True)

    instrucciones = fields.Html(string='Instrucciones', readonly=False)

    fecha_validacion = fields.Date('Fecha Validada', tracking=True,
                                 copy=False, readonly=True, help="Esta es la fecha de visita realizada.")
    date_sampling = fields.Date('Fecha Muestreo', required=False, index=True, readonly=False, help="Esta es la fecha de toma de muestras.")
    worksheet_id = fields.One2many(
        'worksheet_laboratorio', 'x_project_task_id', string='Worksheet ID', readonly=True,
        help="Invoices paid using this mandate.")

    # def action_send_report(self):
    #     res = super().action_send_report()
    #     if 'context' in res:
    #         template_id = self.env.ref('p13n_vatten.vatten_mail_template').id
    #         res['context']['default_use_template'] = bool(template_id)
    #         res['context']['default_template_id'] = template_id

    #     return res

    def action_fsm_validate(self):
        res = super().action_fsm_validate()
        if not self.fecha_validacion:
            raise UserError(_("No se puede marcar como hecho sin antes validar."))
        return res

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('service.order') or _('New')
        result = super(ProjectTask, self).create(vals)
        return result
