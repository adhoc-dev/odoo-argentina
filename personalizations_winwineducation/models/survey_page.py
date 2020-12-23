from odoo import api, fields, models
from odoo.exceptions import UserError

class SurveyPage(models.Model):
    _inherit = 'survey.question'

    show_anchor_partner = fields.Boolean(string='Mostrar ancla en contactos')
    
    def open_anchor(self):
        partner_id = self.env['res.partner'].browse(self._context.get('partner_id'))
        partner_input = self.survey_id.user_input_ids.filtered(lambda x: x.partner_id == partner_id and x.state == 'done').sorted(key=lambda x: x.date_create, reverse=True)
        if not partner_input:
            raise UserError('No encontramos ninguna respuesta en la encuesta "%s" para el alumno "%s"' %(self.survey_id.title, partner_id.name))
        url = partner_input[0].survey_id.print_url + '/' + partner_input[0].token
        if self.sequence != min(self.survey_id.page_ids.mapped('sequence')):
            pagina = self.survey_id.page_ids.filtered(lambda x: x.sequence == (self.sequence - 1))
            ultima_pregunta = max(pagina.question_ids.filtered(lambda x: x.sequence == max(pagina.question_ids.mapped('sequence'))).ids)
            if pagina and ultima_pregunta:
                url += '#' + str(self.survey_id.id) + '_' + str(pagina.id) + '_' + str(ultima_pregunta)

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'}

