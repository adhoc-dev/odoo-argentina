from odoo import models, fields


class ProductAttributeTemplate(models.Model):
    _inherit = 'product.attribute.template'

    x_user_help = fields.Many2one(string="Usuario de ayuda", comodel_name="res.users", help="Usuario asignado para ayuda", on_delete="set null")
    x_studio_field_KdzoJ = fields.Char(string="Orden de preguntas chatbot", copy=False)
    x_chatbot_trained = fields.Boolean(string="Chatbot Entrenado?", copy=False)
    x_simplificado = fields.Boolean(string="Simplificado")
