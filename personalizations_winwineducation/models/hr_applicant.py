from odoo import models, fields


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    x_reference = fields.Char(string="Recomendado por", copy=False)
    x_studio_horas_titulares_en_otras_instituciones = fields.Integer(string="Horas titulares en otras instituciones", copy=False)
    x_studio_disponibilidad_horaria = fields.Selection(string="Disponibilidad Horaria", selection=[["Turno Mañana","Turno Mañana"],["Turno Tarde","Turno Tarde"],["Indistinto","Indistinto"],["Jornada Completa","Jornada Completa"]], copy=False)
    x_studio_domicilio = fields.Char(string="Domicilio", copy=False)
    x_studio_carrera_finalizada = fields.Selection(string="Carrera finalizada", selection=[["Sí","Sí"],["No","No"]], copy=False)
    x_studio_fecha_de_nacimiento = fields.Date(string="Fecha de nacimiento", copy=False)
    x_studio_antigedad_acreditada_en_docencia = fields.Integer(string="Antigüedad acreditada en docencia", copy=False)
    x_studio_conocimiento = fields.Integer(string="Conocimiento", copy=False)
    x_studio_capacidad = fields.Integer(string="Capacidad", copy=False)
    x_studio_honestidad = fields.Integer(string="Honestidad", copy=False)
    x_studio_energa = fields.Integer(string="Energía", copy=False)
    x_appraisal_ids = fields.One2many(string="Evaluaciones", comodel_name="x_hr.applicant.appraisal", inverse_name="x_hr_applicant_id")
    x_date_desired = fields.Date(string="Fecha de Incorporación Deseada")
    x_motive_rejected_proposal_id = fields.Many2one(string="Motivo de la Decisión", comodel_name="x_motive_rejected_proposal", on_delete="set null")
    x_studio_remuneracin_bruta_pretendida = fields.Char(string="Remuneración bruta pretendida", copy=False)
