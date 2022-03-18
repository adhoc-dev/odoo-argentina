from odoo import models, fields
from werkzeug import urls


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    company_id = fields.Many2one('res.company', string="Colegio")

    def get_answer(self, question):
        self.ensure_one()
        response_line = self.user_input_line_ids.filtered(lambda x: x.question_id == question)
        if not response_line or response_line[0].skipped:
            return ''
        answer_field = {
            'text': 'value_text',
            'date': 'value_date',
            'free_text': 'value_free_text',
            'suggestion': 'value_suggested',
            'number': 'value_number',
        }.get(response_line[0].answer_type)
        if answer_field == 'value_suggested':
            return response_line[0].value_suggested.display_name
        if answer_field == 'value_date':
            return response_line[0].value_date.strftime("%d-%m-%Y")
        else:
            return response_line[0][answer_field]

    def _get_survey_url(self):
        """ Este metodo nativamente solo devuelve la url (sin dominio), se termina agregando al dominio desde el cual
        está accediendo al usuario.
        Lo extendemos para que si la user input tiene company, y hay website con dominio para ese company, entonces
        usemos ese dominio. (Similar a lo que hacemos action_start_survey, solo que ese solo afecta desde CRM y este
        se usa en muchas acciones de servidor). """
        self.ensure_one()
        survey_url = super()._get_survey_url()
        website = self.company_id and self.env['website'].search(
            [('company_id', '=', self.company_id.id), ('domain', '!=', False)], limit=1)
        if website:
            survey_url = urls.url_join(website.get_base_url(), survey_url)
        return survey_url
