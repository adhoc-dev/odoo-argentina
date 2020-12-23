from odoo import api, models, fields
from odoo.fields import datetime


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
