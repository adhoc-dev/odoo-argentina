from odoo import models, fields


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    x_chatbot_required = fields.Integer(string="Obligatorio Chatbot", help="Ver si es obligatorio en el chatbot")
    x_chatbot_name = fields.Char(string="Nombre en Chatbot", copy=False)
    x_chatbot_help = fields.Text(string="Ayuda")
    x_chatbot_example = fields.Char(string="Ejemplo")
    x_chatbot_question = fields.Char(string="Pregunta")
