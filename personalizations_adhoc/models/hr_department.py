from odoo import models, fields


class HrDepartment(models.Model):

    _inherit = 'hr.department'
    technical_team_id = fields.One2many('adhoc.product', 'technical_team_id')
