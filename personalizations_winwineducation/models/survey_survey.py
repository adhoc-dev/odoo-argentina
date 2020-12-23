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
        res = super()._create_answer(user=user, partner=partner, email=email, test_entry=test_entry, check_attempts=check_attempts, **additional_vals)
        res.write({'company_id': self.env.company.id})
        return res