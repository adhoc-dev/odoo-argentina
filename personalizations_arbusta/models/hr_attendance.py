from odoo import models, fields


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    x_studio_field_x2oC7 = fields.Selection(string="Oficina", related="employee_id.x_studio_field_HkwZE",
                                            readonly=True, copy=False, store=True)
