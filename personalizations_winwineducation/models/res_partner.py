from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_matricula = fields.Boolean(string="Matricula año próximo", help="Este campo sirve para indicar si el alumno matricula para el año siguiente o no", default=True)
    x_no_matricula_motivo = fields.Selection(string="Motivo no matricula", selection=[('mu','Mudanza'),('pe','Problemas Económicos'),('di','Decisión Institucional'),('re','Repite'),('nh','No le sirve horario'),('ot','Otro')], help="Motivos por el cual el alumno no matricula")
    x_no_matricula_motivo_otros = fields.Text(string="Otros", help="Descripción de cual sería el motivo que no se encuentra en las opciones")
    x_disabled_person_description = fields.Char(string="Descripción de dificultad")
    x_authorized_emergency_contacts = fields.One2many(string="Contacto de Emergencia", comodel_name="x_res.partner.emergency.contact", inverse_name="x_res_partner_id")
    como_conocio_colegio = fields.Selection(string='¿Cómo conoció nuestro colegio?',
                                            selection=[
                                                ('pvp', 'Publicidad en vía pública'),
                                                ('r', 'Recomendación'),('f','Facebook'),
                                                ('i','Instagram'),('bg','Búsqueda en Google')])
    modalidad_pago = fields.Selection(string='Modalidad de pago elegida',
                                      selection=[
                                          ('cuotas', '10 cuotas mensuales + 1 cuota de mantenimiento educativo'),
                                          ('pago_completo', 'Pago único año completo 2021')])
    accede_descuento = fields.Boolean('Accede al beneficio de descuento por hermanos')
    curso_actual = fields.Many2one(comodel_name='academic.group', string='Curso Actual',
                                   compute="_compute_curso_actual", store=True)
    tipo_relacion = fields.Selection(string='Tipo de Relación', selection=[('m', 'Madre'), ('p', 'Padre'),('t','Tutor')])
    enfermedad_requiere_tratamiento = fields.Char(string='Enfermedad que requiere tratamiento médico')
    internado = fields.Boolean(string='¿Fue internado?')
    alergia = fields.Boolean(string='¿Tiene alergía?')
    manifestacion_alergia = fields.Char(string='¿Como se manifiesta')
    recibe_tratamiento = fields.Boolean(string='¿Recibe tratamiento?')
    tratamiento_medico = fields.Char(string='Tratamiento médico')
    tratamiento_quirurgico = fields.Boolean(string='¿Recibe/Recibió tratamiento quirúrgico?')
    edad_tratamiento_quirurgico = fields.Char(string='Edad tratamiento quirurgico')
    tipo_cirugia = fields.Char(string='Tipo de cirugía')
    limitacion_fisica = fields.Char(string='Limitación física')
    otros_problemas_salud = fields.Char(string='Otros problemas de salud')
    semaforo = fields.Selection(string='Semáforo', selection=[('1', '1 Mes'), ('2', '2 Meses'), ('3', '3 Meses'), ('999', '>= 4 Meses')])
    anchored_survey_page_ids = fields.Many2many(comodel_name='survey.question', string='Paginas con ancla', compute="_compute_anchored_pages")
    comment = fields.Html()
    tipo_de_mora = fields.Many2one(string='Causa de Mora', comodel_name='x_account_overdue_type', on_delete="set null")
    x_my_parent_ids = fields.Many2many(comodel_name='res.partner', string='Ids de padres', compute="_compute_parent_ids", readonly= True)
    x_fecha_ultimo_contacto = fields.Date(string="Fecha ultimo contacto", copy=False)

    def _compute_anchored_pages(self):
        self.anchored_survey_page_ids = self.anchored_survey_page_ids.search([('show_anchor_partner', '=', True)])

    @api.depends('student_group_ids')
    def _compute_curso_actual(self):
        for rec in self.filtered(lambda x: x.student_group_ids):
            rec.curso_actual = rec.student_group_ids.sorted(key=lambda r: r.year, reverse=True)[0]

    @api.depends('parent_id')
    def _compute_parent_ids(self):
        for record in self:
            record.x_my_parent_ids = record.parent_id.child_ids.filtered(lambda x: x.partner_type == 'parent')

