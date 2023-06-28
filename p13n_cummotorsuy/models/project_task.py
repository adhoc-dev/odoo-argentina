from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    odometro = fields.Integer(readonly=False)
    cms_uom = fields.Selection(
        [('km','Km'),('horas','Horas'),], readonly=False, string=False)
    lugar_de_reparacion = fields.Selection(
        [('taller','Taller'),('campo','Campo'),], readonly=False)
    distancia_a_campo = fields.Integer(readonly=False)