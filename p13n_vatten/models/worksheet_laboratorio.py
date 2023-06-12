from odoo import models, fields, api, exceptions
import re
import logging

_logger = logging.getLogger(__name__)


class ControlAnalitico(models.Model):
    _description = 'worksheet_laboratorio'
    _name = 'worksheet_laboratorio'
    _rec_name = 'x_project_task_id'

    comments = fields.Text()
    x_project_task_id = fields.Many2one('project.task', required=True,)
    adjuntos = fields.Many2many('ir.attachment', string="Adjuntos", readonly=False)
    order_type = fields.Selection(selection=[('control_de_aguas', 'Control Analítico de Aguas'), (
                                'informe_tecnico', 'Informe Técnico')],
                                default='control_de_aguas',
                                required=True,
                                string='Tipo de Orden',
                                help='Ingrese el tipo de control a realizar')
    recomendaciones = fields.Html(string='Recomendaciones', readonly=False)
    observaciones_inf_tec = fields.Html(string='Observaciones', readonly=False)
    instrucciones = fields.Html(string='Instrucciones', readonly=False)
    imagen1 = fields.Binary(string="Imágen1")
    imagen2 = fields.Binary(string="Imágen2")
    imagen3 = fields.Binary(string="Imágen3")
    imagen4 = fields.Binary(string="Imágen4")

    firma_cliente = fields.Binary(string="Firma y aclaración del Cliente", readonly=False)
    firma_operador = fields.Binary(string="Firma y aclaración del Responsable Técnico", readonly=False)

    determinacion_ids = fields.One2many(
        comodel_name='fsm_determinaciones', inverse_name='order_id',
        compute='_compute_determinaciones', store=True, readonly=False)

    fecha_validacion = fields.Date(related="x_project_task_id.fecha_validacion")
    date_sampling = fields.Date(related="x_project_task_id.date_sampling")

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

    @api.depends('x_project_task_id.lugar_de_servicio')
    def _compute_determinaciones(self):
        for rec in self:
            # borra los registros que haya
            rec.determinacion_ids = False

            # self.update({'determinacion_ids':[(2,individual.id) for individual in self.determinacion_ids]})
            # crea nuevos registros
            r = []
            for muestra in self.env['muestras'].search([('partner_service_id.id', '=', self.x_project_task_id.lugar_de_servicio.id)]).sorted(key=lambda r: r.sequence):
                for parametro in muestra.parametro_ids.sorted(key=lambda r: r.sequence):
                    r.append((0, 0, {
                        'muestra_name': muestra.name.replace(' ', '\N{NO-BREAK SPACE}'),
                        'parametro_name': parametro.chemical_parameter_id.name.replace(' ', '\N{NO-BREAK SPACE}'),
                        'unit_name': parametro.unit.replace(' ', '\N{NO-BREAK SPACE}'),
                        'parametro_display': parametro.chemical_parameter_id.name.replace(' ', '\N{NO-BREAK SPACE}') + '\n' + parametro.chemical_parameter_id.unit.replace(' ', '\N{NO-BREAK SPACE}'),
                        'valor': '',
                        'min_value': parametro.min_value,
                        'max_value': parametro.max_value,
                        'in_report': parametro.in_report,
                        'in_chart': parametro.in_chart,
                        }))
            self.update({'determinacion_ids': r })

    def button_validar(self):

        if self.fecha_validacion:
            raise exceptions.UserError('La orden no se puede volver a validar!')

        if self.order_type == 'control_de_aguas':
            if not len(self.determinacion_ids):
                raise exceptions.UserError('No hay tabla de mediciones!')

            muestras = {}
            total = 0
            for det in self.determinacion_ids:
                if det.muestra_name not in muestras.keys():
                    muestras[det.muestra_name] = {}
                if det.valor:
                    muestras[det.muestra_name][det.parametro_name] = 1
                else:
                    muestras[det.muestra_name][det.parametro_name] = 0
            for key in muestras:
                total += sum(muestras[key].values())
                if len(muestras[key].keys()) != sum(muestras[key].values()) and sum(muestras[key].values()) != 0:
                    raise exceptions.UserError('Falta completrar algun(os) valor(es) de medición!')

            if total == 0:
                raise exceptions.UserError('Falta completrar algun(os) valor(es) de medición!')

        elif self.order_type == 'informe_tecnico':
            if self.check_blank(self.observaciones_inf_tec):
                raise exceptions.UserError('No hay observaciones en el informe técnico!')

        if self.check_blank(self.recomendaciones):
            raise exceptions.UserError('No hay anotaciones en las recomendaciones al cliente!')

        self.x_project_task_id.fecha_validacion = fields.Date.context_today(self)
        # self.filtered(lambda s: s.state == 'draft').write({'state': 'done'})

    def check_blank(self, html_text):
        reg_str = "<p>(.*?)</p>"
        res = re.findall(reg_str, html_text)
        for element in res:
            if element != '<br>':
                for c in element:
                    if c not in [' ', '\xa0']:
                        return False
        return True

    def get_parametros(self, count):
        parametros = self.determinacion_ids.mapped('parametro_name')
        res = parametros[:count]
        return res

    def get_unidad(self, parametro=''):
        if not parametro or parametro == '' or parametro == '-':
            return '-'
        return self.determinacion_ids.filtered(lambda r: r.parametro_name == parametro)[0].unit_name

    def get_valor(self, muestra='', parametro=''):
        if not muestra or muestra == '' or muestra == '-' or not parametro or parametro == '' or parametro == '-':
            return '-'
        return self.determinacion_ids.filtered(lambda r: r.muestra_name == muestra and r.parametro_name == parametro).valor or '-'

    def get_limites(self, muestra='', parametro=''):
        if not muestra or muestra == '' or muestra == '-' or not parametro or parametro == '' or parametro == '-':
            return '-'
        minimo = self.determinacion_ids.filtered(lambda r: r.muestra_name == muestra and r.parametro_name == parametro).min_value
        maximo = self.determinacion_ids.filtered(lambda r: r.muestra_name == muestra and r.parametro_name == parametro).max_value
        res = f' >{minimo}' if minimo else ''
        res += f' <{maximo}' if maximo else ''
        if minimo or maximo:
            res = f'({res})'
        return res or '-'

    def get_muestras(self):
        muestras = self.determinacion_ids.mapped('muestra_name')
        return list(set(muestras))
