from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    name = fields.Char(string='Orden', copy=False, readonly=True,
                       required=True, default=lambda self: _('New'))
    lugar_de_servicio = fields.Many2one('res.partner', string='Lugar de Servicio', help="Dirección donde se prestará el servicio.")
    partner_email = fields.Char(related='partner_id.email', string="Email", readonly=True)
    instrucciones = fields.Html(string='Instrucciones', readonly=False)
    fecha_validacion = fields.Date('Fecha Validada', tracking=True,
                                 copy=False, readonly=True, help="Esta es la fecha de visita realizada.")
    date_sampling = fields.Date('Fecha Muestreo', required=False, index=True, readonly=False, help="Esta es la fecha de toma de muestras.")
    worksheet_id = fields.One2many(
        'worksheet_laboratorio', 'x_project_task_id', string='Worksheet ID', readonly=True,
        help="Invoices paid using this mandate.")

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


    @api.onchange('lugar_de_servicio')
    def _onchange_lugar_de_servicio(self):

        if(not self.lugar_de_servicio):
            return {}

        # borra los registros que haya
        self.worksheet_id.update({'determinacion_ids':[(2,individual.id) for individual in self.worksheet_id.determinacion_ids]})

        # crea nuevos registros
        r=[]
        for muestra in self.env['muestras'].search([('partner_service_id.id', '=', self.lugar_de_servicio.id)]).sorted(key=lambda r: r.sequence):
            for parametro in muestra.parametro_ids.sorted(key=lambda r: r.sequence):
                r.append((0, 0, {
                    'muestra_name': muestra.name.replace(' ','\N{NO-BREAK SPACE}'),
                    'parametro_name': parametro.chemical_parameter_id.name.replace(' ','\N{NO-BREAK SPACE}'),
                    'unit_name': parametro.unit.replace(' ','\N{NO-BREAK SPACE}'),
                    'parametro_display': parametro.chemical_parameter_id.name.replace(' ','\N{NO-BREAK SPACE}') + '\n' + parametro.chemical_parameter_id.unit.replace(' ','\N{NO-BREAK SPACE}'),
                    'valor': '',
                    'min_value': parametro.min_value,
                    'max_value': parametro.max_value,
                    'in_report': parametro.in_report,
                    'in_chart': parametro.in_chart,
                    }))
        self.worksheet_id.update({'determinacion_ids': r })

        # set domain for interlocutor
        self.partner_id = []
        interlocutores =  self.env['res.partner'].search(
                ['&',('type', '=', 'contact'),('parent_id.id','=',self.lugar_de_servicio.id)]
            ).mapped('id')
        res = {'domain' : {'partner_id': [('id', 'in', interlocutores)]}}
        return res
