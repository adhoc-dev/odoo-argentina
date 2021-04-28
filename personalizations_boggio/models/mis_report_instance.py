from odoo import models, fields


class MisReportInstance(models.Model):
    _inherit = 'mis.report.instance'

    x_studio_field_PQwWN = fields.Many2many(string="Usuarios", comodel_name="res.users", relation="x_mis_report_instance_res_users_rel", column1="mis_report_instance_id", column2="res_users_id", copy=False)
