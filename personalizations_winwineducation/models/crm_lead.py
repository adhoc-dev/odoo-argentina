from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_studio_field_zjCR3 = fields.Char(string="New Texto", copy=False)
    x_studio_ao_ingreso = fields.Selection(string="Año Ingreso", selection=[], copy=False)
    x_studio_responsabletutor = fields.Char(string="Responsable/Tutor", copy=False)
    x_studio_alumno = fields.Char(string="Alumno", copy=False)
    x_studio_cmo_nos_conociste = fields.Selection(string="¿Cómo nos conociste?",
                                                  selection=[
                                                            ["Facebook", "Facebook"], ["Instagram", "Instagram"],
                                                            ["Google", "Google"], ["Recomendación", "Recomendación"],
                                                            ["Publicidad en la vía pública",
                                                             "Publicidad en la vía pública"],
                                                            ["Diario Clarín", "Diario Clarín"]], copy=False)
    x_studio_consultas_adicionales = fields.Text(string="Consultas adicionales", copy=False)
    x_studio_ao_ingreso_1 = fields.Char(string="Año Ingreso ", copy=False)
    x_studio_cmo_nos_conociste_1 = fields.Char(string="¿Cómo nos conociste? ", copy=False)
    x_studio_cantidad_de_hijos = fields.Selection(string="Cantidad de hijos", selection=[["1","1"],["2","2"],["3","3"],["4","4"],["5","5"],["6","6"]], copy=False)
    x_studio_field_Ww0WK = fields.Boolean(string="New Casilla de verificación", copy=False)
    x_studio_aos_de_hijos = fields.Selection(string="Años de hijos", selection=[["1ºA","1"],["2","2"],["3","3"],["4","4"],["5","5"],["6","6"]], copy=False)
    x_studio_field_96kG3 = fields.Boolean(string="New Casilla de verificación ", copy=False)
    x_studio_numero_de_documento = fields.Integer(string="N° Documento Hijo", copy=False)
    x_note = fields.Text(string="Nota informativa")
    x_history_stages = fields.Char(string="Historial de etapas", compute="_compute_x_history_stages", help="Muestra de forma cronológica las etapas por las que paso esta Oportun", readonly=True, copy=False, store=True)
    x_studio_n_documento_padre = fields.Integer(string="N° Documento Padre", copy=False)
    x_studio_prioridad_de_contacto = fields.Char(string="Prioridad de contacto", copy=False)
    x_student_country_id = fields.Many2one(string="Nacionalidad", comodel_name="res.country", on_delete="set null")
    x_mother_country_id = fields.Many2one(string="Nacionalidad Madre", comodel_name="res.country", on_delete="set null")
    x_father_country_id = fields.Many2one(string="Nacionalidad Padre", comodel_name="res.country", on_delete="set null")
    x_studio_n_documento_madre = fields.Integer(string="N° Documento Madre")
    x_student_birthdate = fields.Date(string="Fecha de Nacimiento")
    x_mother_birthdate = fields.Date(string="Fecha de Nacimiento Madre")
    x_father_birthdate = fields.Date(string="Fecha de Nacimiento Padre")
    x_father_profession = fields.Char(string="Profesión/Ocupación Padre")
    x_mother_profession = fields.Char(string="Profesión/Ocupación Madre")
    x_father_act_condition = fields.Selection(string="Condición de la Actividad Padre", selection=[('tp','Trabajo Permanente'),('tt','Trabajo Temporario'),('am','Ama de Casa'),('jp','Jubilado/Pensionado'),('d','Discapacitado'),('o','Otros')])
    x_mother_act_condition = fields.Selection(string="Condición de la Actividad Madre", selection=[('tp','Trabajo Permanente'),('tt','Trabajo Temporario'),('am','Ama de Casa'),('jp','Jubilado/Pensionado'),('d','Discapacitado'),('o','Otros')])
    x_father_phone = fields.Char(string="Teléfono Padre")
    x_mother_phone = fields.Char(string="Teléfono Madre")
    x_father_first_name = fields.Char(string="Nombre Padre")
    x_mother_first_name = fields.Char(string="Nombre Madre")
    x_father_last_name = fields.Char(string="Apellido Padre")
    x_mother_last_name = fields.Char(string="Apellido Madre")
    x_establishment = fields.Char(string="Establecimiento")
    x_transfer_reason = fields.Char(string="Motivo del Pase")
    x_companions_relationship = fields.Char(string="¿Como es la relación con sus compañeros?")
    x_difficulties_workarea = fields.Selection(string="¿Presenta dificultades en las áreas de trabajo?", selection=[('si','Si'),('no','No')])
    x_difficulties_workarea_description = fields.Text(string="Describa")
    x_areas_student_standout = fields.Char(string="¿En qué áreas se destaca?")
    x_motive_no_vacancy = fields.Selection(string="Motivo", selection=[('d', 'Diagnóstico'),('pd', 'Posible Diagnóstico'),('se', 'Situación Económica')])
    x_motive_no_vacancy_specification_id = fields.Many2one(string="Especificación", comodel_name="x_no_vacancy_specification_motive", on_delete="set null")
    x_type = fields.Selection(string="Tipo de equipo", related="team_id.x_type", readonly=True, copy=False, store=True)
    x_mother_nosis = fields.Char(string="Nosis Madre")
    x_father_nosis = fields.Char(string="Nosis Padre")
    x_mother_approve = fields.Selection(string="Aprueba excepción Madre", selection=[('si', 'Si'),('no','No')])
    x_father_approve = fields.Selection(string="Aprueba excepción Padre", selection=[('si', 'Si'),('no','No')])


    @api.depends('message_ids.tracking_value_ids')
    def _compute_x_history_stages(self):
        for rec in self.filtered(lambda x: any(x.sudo().message_ids.mapped('tracking_value_ids').filtered(lambda x: x.field == 'stage_id'))):
            msj =" > ".join(rec.sudo().message_ids.mapped('tracking_value_ids').filtered(lambda x: x.field == 'stage_id').sorted(key=lambda p: p.create_date).mapped('new_value_char'))
            rec['x_history_stages'] = msj
