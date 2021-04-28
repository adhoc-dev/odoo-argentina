from odoo import models, fields


class ProjectTags(models.Model):
    _inherit = 'project.tags'

    x_prioridad = fields.Float(string="Prioridad", help="valores de 1 a 5", copy=False)
