from odoo import models


class HrEmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    def action_open_employee(self):
        """ ticket #34761. Boton para abrir el empleado desde la vista lista de Nivel de habilidad para un empleado """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'res_id': self.employee_id.id,
        }
