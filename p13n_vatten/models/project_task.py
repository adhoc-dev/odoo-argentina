from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    partner_email = fields.Char(related='partner_id.email', string="Email", readonly=True)

    instrucciones = fields.Html(string='Instrucciones', readonly=False)

    fecha_validacion = fields.Date('Fecha Validada', tracking=True,
                                 copy=False, readonly=True, help="Esta es la fecha de visita realizada.")
    date_sampling = fields.Date('Fecha Muestreo', required=False, index=True, readonly=False, help="Esta es la fecha de toma de muestras.")
    worksheet_id = fields.One2many(
        'worksheet_control_analitico_agua', 'x_project_task_id', string='Worksheet ID', readonly=True,
        help="Invoices paid using this mandate.")



    # adjuntos = fields.Many2many('ir.attachment', string="Adjuntos", readonly=False)

    # order_type = fields.Selection(selection=[('control_de_aguas', 'Control Analítico de Aguas'),
    #                                          #                                             ('control_de_efluentes', 'Control Analítico de Efluentes'),
    #                                          #                                             ('control_de_corrosion', 'Medición de Tasa de Corrosión'),
    #                                          ('informe_tecnico', 'Informe Técnico')],
    #                               default='control_de_aguas',
    #                               required=True,
    #                               tracking=True,
    #                               string='Tipo de Orden',
    #                               help='Ingrese el tipo de control a realizar')
    # recomendaciones = fields.Html(string='Recomendaciones', tracking=True,
    #                               readonly=False)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('project.task') or _('New')
    #     result = super(ProjectTask, self).create(vals)
    #     return result

    def action_send_report(self):
        res = super().action_send_report()
        if 'context' in res:
            template_id = self.env.ref('p13n_vatten.vatten_mail_template').id
            res['context']['default_use_template'] = bool(template_id)
            res['context']['default_template_id'] = template_id

        return res