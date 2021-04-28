from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_texto = fields.Text(string="Texto sin formato")
    x_impacto = fields.Float(string="Impacto", readonly=True, copy=False)
    x_objetive = fields.Many2one(string="Objetivo", comodel_name="res.partner.industry", domain="[('x_objetivos', '=', True)]", on_delete="set null")
    x_score = fields.Float(string="Puntuacion")
