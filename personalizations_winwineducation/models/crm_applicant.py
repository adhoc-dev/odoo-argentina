from odoo import  models


class Applicant(models.Model):
    _inherit = "crm.lead"

    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            # use link as type in order to avoid deletion of records
            # that they wasn't started yet made by 'do_clean_emptys' method
            response = self.env['survey.user_input'].with_context(default_type="link").create(
                {'survey_id': self.survey_id.id,
                    'partner_id': self.partner_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(
            survey_token=response.token, allowed_company_ids=[self.company_id.id]).action_start_survey()
