from odoo import models, fields


class MailMassMailingContact(models.Model):
    _inherit = 'mailing.contact'

    x_cant_inscripciones = fields.Integer(string="Cantidad de inscripciones", help="Cantidad de inscripciones a cursos")
    x_cant_asistencias = fields.Integer(string="Cantidad de Asistencias", help="Cantidad de asistencias a cursos")
