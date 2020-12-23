from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'

    x_date_desired = fields.Date(string="Fecha de Incorporación Deseada")
