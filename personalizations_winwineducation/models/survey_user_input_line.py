from odoo import models, fields


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    x_id_question = fields.Integer(string="id pregunta", related="question_id.id", readonly=True, copy=False, store=True)
