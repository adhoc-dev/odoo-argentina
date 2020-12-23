from odoo import models, fields, api


class XHrApplicantAppraisal(models.Model):
    _name = 'x_hr.applicant.appraisal'
    _description = 'Proceso de Evaluación'

    x_partner_id = fields.Many2one(string="Entrevistador", comodel_name="res.partner", on_delete="cascade", required=True)
    x_energy = fields.Integer(string="Energía")
    x_capability = fields.Integer(string="Capacidad")
    x_honesty = fields.Integer(string="Honestidad")
    x_knowledge = fields.Integer(string="Conocimiento")
    x_hr_applicant_id = fields.Many2one(string="Solicitud", comodel_name="hr.applicant", on_delete="set null")
    x_applicant_stage_id = fields.Many2one(string="Etapa Para Evaluacion", comodel_name="hr.recruitment.stage", compute="_compute_x_applicant_stage_id", on_delete="set null", readonly=True, copy=False)
    x_atual_stage = fields.Boolean(string="Etapa Actual", compute="_compute_x_atual_stage", readonly=True, copy=False)

    @api.depends('x_hr_applicant_id')
    def _compute_x_applicant_stage_id(self):
        for record in self:
          record.x_applicant_stage_id = False
          if isinstance(record.id, int):
            if record.x_hr_applicant_id.x_appraisal_ids.ids.index(record.id) == 0:
               record.x_applicant_stage_id = 2
            elif record.x_hr_applicant_id.x_appraisal_ids.ids.index(record.id) == 1:
              record.x_applicant_stage_id = 3
            elif record.x_hr_applicant_id.x_appraisal_ids.ids.index(record.id) == 2:
              record.x_applicant_stage_id = 6
            elif record.x_hr_applicant_id.x_appraisal_ids.ids.index(record.id) == 3:
              record.x_applicant_stage_id = 12
            elif record.x_hr_applicant_id.x_appraisal_ids.ids.index(record.id) == 4:
              record.x_applicant_stage_id = 13


    @api.depends('x_applicant_stage_id')
    def _compute_x_atual_stage(self):
        for record in self:
          record.x_atual_stage = False
          if isinstance(record.id, int):
            if record.x_applicant_stage_id and record.x_applicant_stage_id == record.x_hr_applicant_id.stage_id:
              record.x_atual_stage = True
