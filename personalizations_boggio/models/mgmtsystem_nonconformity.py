from odoo import models, fields


class MgmtsystemNonconformity(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    x_etiqueta = fields.Many2many(string="Etiqueta", comodel_name="project.tags", relation="x_mgmtsystem_nonconformity_project_tags_rel", column1="mgmtsystem_nonconformity_id", column2="project_tags_id", help="Etiqueta")
    x_origen_no_conformidad = fields.Many2one(string="¿Dónde ocurrió el desvío?", comodel_name="x_origen_tags", help="Sector en el cual se produjo el error.")
    x_impacto = fields.Float(string="Impacto", readonly=True, copy=False)
