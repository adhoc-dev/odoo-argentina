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
            answer.company_id = partner.company_id.id if partner and partner.company_id else self.env.company.id
        return answers

    def _compute_survey_url(self):
        """ Modificamos este metodo para permitir recibir por contexto una website_domain que tipicamente sera la url
        de un determinado sitio web.
        Por ahora esta solo implementado en crm.lead en el metodo de action_start_survey """
        super()._compute_survey_url()
        if self._context.get('website_domain'):
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            website_domain = self._context.get('website_domain')
            for survey in self:
                survey.public_url = survey.public_url.replace(base_url, website_domain)
