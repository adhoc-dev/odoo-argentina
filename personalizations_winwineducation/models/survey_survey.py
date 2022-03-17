##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields
from odoo.exceptions import UserError


class SurveySurvey(models.Model):

    _inherit = 'survey.survey'

    x_shared_survey_internally = fields.Boolean(string='Compartir respuestas de la encuesta internamente', help="Tildando esta opción, los usuarios con permisos de planificación básicos van a poder ver todas las respuestas de esta encuesta")

    def _create_answer(self, user=False, partner=False, email=False, test_entry=False, check_attempts=True, **additional_vals):
        answers = super()._create_answer(user=user, partner=partner, email=email, test_entry=test_entry, check_attempts=check_attempts, **additional_vals)
        for answer in answers.filtered(lambda x: not x.company_id):
            answer.company_id = partner.company_id.id or self.env.company.id
        return answers
