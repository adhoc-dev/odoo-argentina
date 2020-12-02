from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_studio_field_NJxF6 = fields.Integer(string="id_odoo8", copy=False)
    x_stage_id = fields.Many2one(string="Etapa", comodel_name="x_res.partner_stage", on_delete="set null", copy=False)
    x_studio_field_Gjamn = fields.Datetime(string="Fecha nacimiento", copy=False)
    x_studio_field_HZyaK = fields.Date(string="Fecha Nacimiento", copy=False)
    x_studio_field_PCg5t = fields.Selection(string="Género", selection=[['Femenino', 'Femenino'], ['Masculino', 'Masculino']], copy=False)
