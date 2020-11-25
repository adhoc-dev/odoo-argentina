from odoo import models, fields


class XProject(models.Model):
    _name = 'x_project'
    _description = 'Logos digital'

    x_name = fields.Char(string="Name", copy=False)
    x_campaign_id = fields.Many2one(string="Campaña", comodel_name="utm.campaign", on_delete="set null")
    x_moodle_code = fields.Text(string="Código Moodle")
    x_partner_id = fields.Many2one(string="Contacto", comodel_name="res.partner", on_delete="set null")
    x_project_ids = fields.Text(string="Proyectos")
