# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from odoo import exceptions
import re

import logging
_logger = logging.getLogger(__name__)

class Parametros(models.Model):
    _description = 'Parametros'
    _name = 'parametros'
    _order = "sequence,id"

    sequence = fields.Integer(string='Secuencia')
    muestra_id = fields.Many2one(comodel_name='muestras', ondelete='cascade')
    name = fields.Many2one(comodel_name='chemical.parameter', string='Parámetro', required=True)
    unit = fields.Char(string='Unidad', readonly=False, store=True, related="name.unit")
    min_value = fields.Char(string='Mínimo')
    max_value = fields.Char(string='Máximo')
    in_report = fields.Boolean(string='Se reporta', default=True)
    in_chart = fields.Boolean(string='Se grafica')

class Muestras(models.Model):
    _description = 'Muestras X'
    _name = 'muestras'
    _order = "sequence,id"

    sequence = fields.Integer(string='Secuencia')
    sample_type = fields.Selection(string='Tipo de Muestra', selection=[('Agua', 'Agua'),('Efluente', 'Efluente')], default='Agua')
    name = fields.Char(string='Punto de Muestreo', required='false', help='Asigne un nombre al punto de muestreo.')
    partner_service_id = fields.Many2one(comodel_name='res.partner', string='Dirección de Servicio', required="true", ondelete='cascade', help="Dirección donde se prestará el servicio.")
    parametro_ids = fields.One2many(comodel_name='parametros', inverse_name='muestra_id', string="Parámetros", copy=True)

    @api.model
    def default_get(self, fields):
        res = super(Muestras, self).default_get(fields)

        recs = self.env['chemical.parameter'].search([('sample_type', '=', 'Agua')], limit=11)

        r=[]
        for rec in recs:
            r.append((0, 0, {'name': rec.id, 'unit': rec.unit, 'in_report': True}))
        res["parametro_ids"] = r

        return res
    
class Determinaciones(models.Model):
    _description = 'Determinaciones'
    _name = 'determinaciones'

    order_id = fields.Many2one(comodel_name='service.order', ondelete='cascade')
    muestra_name = fields.Char(string='Muestra')
    parametro_name = fields.Char(string='Parámetro')
    unit_name = fields.Char(string='Unidad')
    parametro_display = fields.Char(string='Parámetro+Unidad')
    valor = fields.Char(string='Valor', default=None)
    min_value = fields.Char(string='Mínimo')
    max_value = fields.Char(string='Máximo')
    in_report = fields.Boolean(string='Se reporta')
    in_chart = fields.Boolean(string='Se grafica')

class ServiceOrder(models.Model):
    _name = 'service.order'
    _description = 'Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc, date_scheduled desc'

    name = fields.Char(string='Orden', copy=False, readonly=True,
                       required=True, default=lambda self: _('New'))
#    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True, required=False, change_default=True, index=True, tracking=True, track_sequence=1)
    partner_service_id = fields.Many2one('res.partner', string='Lugar de Servicio', required=True, tracking=True, readonly=True, states={
                                         'draft': [('readonly', False)]}, help="Dirección donde se prestará el servicio.")
    partner_name = fields.Char(related='partner_service_id.name')
    parent_id = fields.Many2one('res.partner', string='Cliente', related='partner_service_id.parent_id')
    direccion = fields.Char(compute='_compute_address')
    reference = fields.Char(string='Referencia', readonly=True, states={
                            'draft': [('readonly', False)]})
    date_created = fields.Datetime(string='Fecha Creada', readonly=True,
                                   required=True, index=True, copy=False, default=fields.Datetime.now)
    date_scheduled = fields.Date('Fecha Programada', required=True, index=True, tracking=True, readonly=True, states={
                                 'draft': [('readonly', False)]}, copy=False, help="Esta es la fecha de visita programada.")
    date_sampling = fields.Date('Fecha Muestreo', required=False, index=True, tracking=True, readonly=True, states={
                                 'draft': [('readonly', False)]}, copy=False, help="Esta es la fecha de toma de muestras.")
    date_validated = fields.Date('Fecha Validada', tracking=True,
                                 copy=False, readonly=True, help="Esta es la fecha de visita realizada.")
    operator = fields.Many2one("res.users", string="Responsable Técnico", required=True, tracking=True, domain=lambda self: [("groups_id", "=", self.env.ref(
        "p13n_vatten.labo_group_user").id)], readonly=True, states={'draft': [('readonly', False)]})
    interlocutor = fields.Many2one("res.partner", string="Interlocutor", required=True,
                                   tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    con_copia_a = fields.Many2one("res.partner", string="Copia a",
                                   tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    mail_interlocutor = fields.Char(string="Mail", required=True, tracking=True, readonly=True, states={'draft': [('readonly', False)]}, default='')
    mail_con_copia_a = fields.Char(string="Copia a")
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Validada'), ('sent', 'Enviada'), (
        'cancel', 'Cancelada')], required=True, tracking=True, default='draft', string='Estado')
    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('laboratory'))
    user_id = fields.Many2one(
        'res.users', 'Current User', default=lambda self: self.env.user)
    order_type = fields.Selection(selection=[('control_de_aguas', 'Control Analítico de Aguas'),
                                             #                                             ('control_de_efluentes', 'Control Analítico de Efluentes'),
                                             #                                             ('control_de_corrosion', 'Medición de Tasa de Corrosión'),
                                             ('informe_tecnico', 'Informe Técnico')],
                                  default='control_de_aguas',
                                  required=True,
                                  tracking=True,
                                  readonly=True, states={'draft': [('readonly', False)]},
                                  string='Tipo de Orden',
                                  help='Ingrese el tipo de control a realizar')

    mediciones2 = fields.Html(string='Mediciones2', tracking=True,
                              readonly=True, states={'draft': [('readonly', False)]})
    mediciones3 = fields.Html(string='Mediciones3', tracking=True,
                              readonly=True, states={'draft': [('readonly', False)]})
    mediciones4 = fields.Html(string='Mediciones4', tracking=True,
                              readonly=True, states={'draft': [('readonly', False)]})
    instrucciones = fields.Html(string='Instrucciones', readonly=True, states={
                                'draft': [('readonly', False)]})
    adjuntos = fields.Many2many('ir.attachment', string="Adjuntos", readonly=True, states={
                                'draft': [('readonly', False)]})

    determinacion_ids = fields.One2many(comodel_name='determinaciones', inverse_name='order_id',
                                        tracking=True, readonly=True, states={'draft': [('readonly', False)]})

    recomendaciones = fields.Html(string='Recomendaciones', tracking=True,
                                  readonly=True, states={'draft': [('readonly', False)]})
    imagenes1 = fields.Binary(string="Imágen1")
    imagenes2 = fields.Binary(string="Imágen2")
    imagenes3 = fields.Binary(string="Imágen3")
    imagenes4 = fields.Binary(string="Imágen4")
    firma_cliente = fields.Binary(string="Firma y aclaración del Cliente", readonly=True, states={
                                  'draft': [('readonly', False)]})
    firma_operador = fields.Binary(string="Firma y aclaración del Responsable Técnico", readonly=True, states={
                                   'draft': [('readonly', False)]})

    @api.depends('partner_service_id')
    def _compute_address(self):
        self.direccion = ''
        if self.partner_service_id:
            if self.partner_service_id.street:
                self.direccion = self.partner_service_id.street
            if self.partner_service_id.street and self.partner_service_id.zip or self.partner_service_id.city:
                self.direccion += ' - '
            if self.partner_service_id.city:
                self.direccion += self.partner_service_id.city
            if self.partner_service_id.zip:
                self.direccion += ' (' + self.partner_service_id.zip + ')'
            if self.partner_service_id.state_id:
                self.direccion += ' - ' + self.partner_service_id.state_id.name
            if self.partner_service_id.country_id:
                self.direccion += ' - ' + self.partner_service_id.country_id.name

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('service.order') or _('New')
        result = super(ServiceOrder, self).create(vals)
        return result

    def write(self, vals):
        res = super(ServiceOrder, self).write(vals)
        return(res)

    def unlink(self):
        for order in self:
            if order.state not in ('draft'):
                raise exceptions.UserError('No se puede eliminar una orden validada, ya enviada al cliente o cancelada!') 
            return super(ServiceOrder, self).unlink()

    def zap(self):
        return super(ServiceOrder, self).unlink()

    def print_service_order(self):
        return self.env.ref('laboratory.action_report_service_order').report_action(self)


#    def email_service_order(self):
#        if self.state not in ['done']:
#            raise exceptions.UserError('No se puede enviar una orden no validada!') 
#        template = self.env.ref('laboratory.mail_template_report')
#        return self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)

    def email_service_order(self):
        self.ensure_one()

        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('laboratory', 'mail_template_report')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': {
               'default_model': 'service.order',
               'default_res_id': self.ids[0],
               'default_use_template': bool(template_id),
               'default_template_id': template_id,
               'default_composition_mode': 'comment',
            }
        }

    def button_validar(self):

        if self.state in ['done','sent','cancel']:
            raise exceptions.UserError('La orden no se puede validar!')

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
            if self.mediciones4 == '<p><br></p>' or self.mediciones4.isspace():
                raise exceptions.UserError('No hay observaciones en el informe técnico!')

        if self.recomendaciones == '<p><br></p>' or self.recomendaciones.isspace():
            raise exceptions.UserError('No hay anotaciones en las recomendaciones al cliente!')

        self.date_validated = fields.Date.context_today(self)
        self.filtered(lambda s: s.state == 'draft').write({'state': 'done'})

    def button_reset(self):
        if self.state in ['sent','cancel']:
            raise exceptions.UserError('No se puede volver a borrador una orden ya enviada al cliente o cancelada!')
        self.date_validated = None
        self.filtered(lambda s: s.state not in ['draft','sent']).write({'state': 'draft'})

    def button_cancel(self):
        if self.state in ['sent']:
            raise exceptions.UserError('No se puede cancelar una orden ya enviada al cliente!')
        self.filtered(lambda s: s.state not in ['sent']).write({'state': 'cancel'})

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
#        for det in self.determinacion_ids:
#            if det.parametro_name in ['AlcF','AlcM','AlcOH']:
#                print(det.parametro_name, ' -> ', det.valor)
#        print('---------------------------------------------')
#        return {'type':'ir.actions.client','tag':'reload',}

    @api.onchange('date_scheduled')
    def _onchange_date_scheduled(self):
        if self.date_scheduled:
            if self.date_scheduled.strftime('%Y-%m-%d') < datetime.now().date().strftime('%Y-%m-%d'):
                return {
                    'warning': {
                        'title': 'Atención!',
                        'message': 'La fecha programada es anterior a hoy.',
                    }
                }

    @api.onchange('partner_service_id')
    def _onchange_partner_service_id(self):

        if(not self.partner_service_id):
            return {}
        print('>>> onchange partner_service_id <<<')

        # borra los registros que haya
        self.update({'determinacion_ids':[(2,individual.id) for individual in self.determinacion_ids]})

        # crea nuevos registros
        r=[]
        for muestra in self.env['muestras'].search([('partner_service_id.id', '=', self.partner_service_id.id)]).sorted(key=lambda r: r.sequence):
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

        # set domain for interlocutor
        self.interlocutor = []
        self.con_copia_a = []
        interlocutores =  self.env['res.partner'].search(
                ['&',('type', '=', 'contact'),'|',('parent_id.id','=',self.partner_service_id.id),('parent_id.id','=',self.partner_service_id.parent_id.id)]
            ).mapped('id')
        res = {'domain' : {'interlocutor': [('id', 'in', interlocutores)],'con_copia_a': [('id', 'in', interlocutores)]}}
        return res

    @api.onchange('interlocutor')
    def _onchange_interlocutor(self):
        self.mail_interlocutor = self.interlocutor.email
        interlocutores =  self.env['res.partner'].search(
                ['&',('type', '=', 'contact'),'|',('parent_id.id','=',self.partner_service_id.id),('parent_id.id','=',self.partner_service_id.parent_id.id)]
            ).mapped('id')
        if self.interlocutor.id and self.interlocutor.id in interlocutores:
            interlocutores.remove(self.interlocutor.id)
        res = {'domain' : {'con_copia_a': [('id', 'in', interlocutores)]}}
        return res

    #jok falta digital_signature por falta dependencia
    # @api.onchange('operator')
    # def _onchange_operator(self):
    #     print('>>>>>>>>>>>>>> ??????? ')
        
    #     if not self.firma_operador:
    #         temp = self.env['res.users'].search([('id', '=', self.operator.id)]).digital_signature
    #         if temp:
    #             self.firma_operador = temp

# Ya estaba comentado TODO: sacar       
#        print('>>> operator id: ', self.operator.id)
#        print('&&&: ', self.env['res.users'].search([('id', '=', self.operator.id)]).digital_signature)
#        print('>>> val firma: ', self.firma_operador)

        return

    @api.onchange('con_copia_a')
    def _onchange_con_copia_a(self):
        self.mail_con_copia_a = self.con_copia_a.email

    @api.onchange('order_type')
    def _onchange_order_type(self):

        if(not self.partner_service_id):
            return {}
        print('>>> onchange order_type <<<')

        if self.order_type == 'control_de_aguas':
            self.mediciones4 = None 
        elif self.order_type == 'informe_tecnico':
            # borra los registros que haya
#            self.update({'determinacion_ids':[(2,individual.id) for individual in self.determinacion_ids]})
            print('>>>>>>>>>>> borra registros')

    def get_muestras(self, count):
        muestras = self.determinacion_ids.mapped('muestra_name')
        lookup = set()
        muestras = [x for x in muestras if x not in lookup and lookup.add(x) is None]
        lmuestras = len(muestras)
        res = []
        for i in range(count):
            if i < lmuestras:
                res.append(muestras[i])
            else:
                res.append('-')
        return(res)

    def get_parametros(self, count):
        parametros = self.determinacion_ids.mapped('parametro_name')
        lookup = set()
        parametros = [x for x in parametros if x not in lookup and lookup.add(x) is None]
        lparametros = len(parametros)
        res = []
        for i in range(count):
            if i < lparametros:
                res.append(parametros[i])
            else:
                res.append('-')
        return(res)

    def get_unidad(self, parametro=''):
        if not parametro or parametro == '' or parametro == '-':
            return('-')
        return(self.determinacion_ids.filtered(lambda r: r.parametro_name == parametro)[0].unit_name)

    def get_valor(self, muestra='', parametro=''):
        if not muestra or muestra == '' or muestra == '-' or not parametro or parametro == '' or parametro == '-':
            return('-')
        return(self.determinacion_ids.filtered(lambda r: r.muestra_name == muestra and r.parametro_name == parametro).valor or '-')

    def get_limites(self, muestra='', parametro=''):
        if not muestra or muestra == '' or muestra == '-' or not parametro or parametro == '' or parametro == '-':
            return('-')
        minimo = (self.determinacion_ids.filtered(lambda r: r.muestra_name == muestra and r.parametro_name == parametro).min_value)
        maximo = (self.determinacion_ids.filtered(lambda r: r.muestra_name == muestra and r.parametro_name == parametro).max_value)
#        print('minimo', minimo)
#        print('maximo', maximo)
        res = ''
        if minimo or maximo:
            res += '('
        if minimo:
            res += '>' + str(minimo)
        if minimo and maximo:
            res += ' '
        if maximo:
            res += '<' + str(maximo)
        if minimo or maximo:
            res += ')'
        return(res or '-')

class LaboratoryReport(models.AbstractModel):
    _name = 'report.laboratory.reporte_protocolo'
    _description = 'Imprime informe de orden de servicio'

    @api.model
    def _get_report_values(self, docids, data=None):
        reporte = self.env['ir.actions.report']._get_report_from_name('laboratory.reporte_protocolo')
        docs = self.env[reporte.model].browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': reporte.model,
            'docs': docs,
        }
        return docargs
