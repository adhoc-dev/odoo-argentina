from odoo import models, fields


class XPartnerProject(models.Model):
    _name = 'x_partner_project'
    _description = 'Proyectos por compañía'

    x_name = fields.Char(string="Name", copy=False)
    x_campaign_id = fields.Many2one(string="Campaña", comodel_name="utm.campaign", on_delete="set null")
    x_partner_id = fields.Many2one(string="Contacto", comodel_name="res.partner", on_delete="set null")
    x_project_ids = fields.Many2many(string="Proyectos", comodel_name="x_project", relation="x_x_partner_project_x_project_rel", column1="x_partner_project_id", column2="x_project_id")
    x_country_id = fields.Many2one(string="País", related="x_partner_id.country_id", on_delete="set null", readonly=True, copy=False, store=True)
    x_state = fields.Many2one(string="Provincia", related="x_partner_id.state_id", on_delete="set null", readonly=True, store=True)
    x_user_id = fields.Many2one(string="Comercial", related="x_partner_id.user_id", help="The internal user that is in charge of communicating with this contact if any.", on_delete="set null", readonly=True, store=True)
