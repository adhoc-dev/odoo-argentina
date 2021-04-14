from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_studio_field_J1l99 = fields.Char(string="URL de Calendar", copy=False)
    x_studio_field_sFveY = fields.Selection(string="Tipo de evento",
                                            selection=[('desayunar', 'desayunar'), ('merendar', 'merendar')],
                                            copy=False)
    x_studio_field_ppIPV = fields.Many2one(string="Tarea", comodel_name="project.task",
                                           on_delete="set null", copy=False)
    x_studio_field_HeGMm = fields.Integer(string="New Número entero", readonly=True, copy=False)
