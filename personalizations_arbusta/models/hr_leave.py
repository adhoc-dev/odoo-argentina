from odoo import models, fields


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    x_studio_field_hJSGA = fields.Date(string="Reincorporación", copy=False)
    x_studio_field_zhYys = fields.Text(string="Comentario ausencia", copy=False)
    x_studio_field_81Rd7 = fields.Char(string="Legajo N°", related="employee_id.x_studio_field_lhpTm",
                                       readonly=True, copy=False, store=True)
    x_studio_field_KpJ0Q = fields.Char(string="Working Hours", related="employee_id.resource_calendar_id.name",
                                       readonly=True, copy=False, store=True)
    x_studio_field_5NlsG = fields.Char(string="Departamento", related="department_id.name",
                                       readonly=True, copy=False, store=True)
    x_studio_field_S5NJG = fields.Many2one(string="Ausencias", comodel_name="hr.employee", on_delete="set null")
