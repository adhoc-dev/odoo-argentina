# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ControlAnalitico(models.Model):
    _description = 'worksheet_control_analitico_agua'
    _name = 'worksheet_control_analitico_agua'

    comments = fields.Text()
    x_project_task_id = fields.Many2one('project.task', required=True,)
    name = fields.Char(compute="_compute_worksheet_name")
    adjuntos = fields.Many2many('ir.attachment', string="Adjuntos", readonly=False)
    order_type = fields.Selection(selection=[('control_de_aguas', 'Control Analítico de Aguas'), (
                                'informe_tecnico', 'Informe Técnico')],
                                default='control_de_aguas',
                                required=True,
                                string='Tipo de Orden',
                                help='Ingrese el tipo de control a realizar')
    recomendaciones = fields.Html(string='Recomendaciones', tracking=True,
                                  readonly=False)
    instrucciones = fields.Html(string='Instrucciones', readonly=False)
    imagen1 = fields.Binary(string="Imágen1")
    imagen2 = fields.Binary(string="Imágen2")
    imagen3 = fields.Binary(string="Imágen3")
    imagen4 = fields.Binary(string="Imágen4")

    firma_cliente = fields.Binary(string="Firma y aclaración del Cliente", readonly=False)
    firma_operador = fields.Binary(string="Firma y aclaración del Responsable Técnico", readonly=False)

    # TODO agrega tracking? necesario?
    determinacion_ids = fields.One2many(
        comodel_name='fsm_determinaciones', inverse_name='order_id',
        compute='_compute_determinaciones', store=True, readonly=False)

    @api.onchange('determinacion_ids')
    def _onchange_determinacion_ids(self):
        alcalinidades = {}
        for det in self.determinacion_ids:
            det.parametro_name = "".join(det.parametro_name.split())
            if det.muestra_name not in alcalinidades.keys():
                alcalinidades[det.muestra_name] = {}
            if det.parametro_name == "AlcF" and det.valor:
                alcalinidades[det.muestra_name][det.parametro_name] = det.valor
            if det.parametro_name == 'AlcM' and det.valor:
                alcalinidades[det.muestra_name][det.parametro_name] = det.valor
            if det.parametro_name == 'AlcOH' and det.valor:
                alcalinidades[det.muestra_name][det.parametro_name] = det
        for key in alcalinidades.keys():
            if len((alcalinidades[key].keys())) == 3:
                AlcF = int(alcalinidades[key]['AlcF'])
                AlcM = int(alcalinidades[key]['AlcM'])
                AlcOH = 2 * AlcF - AlcM
                if AlcOH < 0:
                    AlcOH = 0
                alcalinidades[key]['AlcOH'].valor = str(AlcOH)

    @api.depends('x_project_task_id.name')
    def _compute_worksheet_name(self):
        for rec in self:
            rec.name = rec.x_project_task_id.name

    @api.depends('x_project_task_id.partner_id')
    def _compute_determinaciones(self):
        for rec in self:
            # borra los registros que haya
            rec.determinacion_ids = False

            # self.update({'determinacion_ids':[(2,individual.id) for individual in self.determinacion_ids]})
            # crea nuevos registros
            r=[]
            for muestra in self.env['muestras'].search([('partner_service_id.id', '=', self.x_project_task_id.partner_id.parent_id.id)]).sorted(key=lambda r: r.sequence):
                for parametro in muestra.parametro_ids.sorted(key=lambda r: r.sequence):
                    r.append((0, 0, {
                        'muestra_name': muestra.name.replace(' ','\N{NO-BREAK SPACE}'),
                        'parametro_name': parametro.name.name.replace(' ','\N{NO-BREAK SPACE}'),
                        'unit_name': parametro.unit.replace(' ','\N{NO-BREAK SPACE}'),
                        'parametro_display': parametro.name.name.replace(' ','\N{NO-BREAK SPACE}') + '\n' + parametro.name.unit.replace(' ','\N{NO-BREAK SPACE}'),
                        'valor': '',
                        'min_value': parametro.min_value,
                        'max_value': parametro.max_value,
                        'in_report': parametro.in_report,
                        'in_chart': parametro.in_chart,
                        }))
            self.update({'determinacion_ids': r })
