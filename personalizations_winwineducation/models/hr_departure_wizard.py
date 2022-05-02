from odoo import api, fields, models


class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    departure_date = fields.Date(string="Fecha de salida")

    def action_register_departure(self):
        employee = self.employee_id
        employee.departure_reason = self.departure_reason
        employee.departure_description = self.departure_description
        employee.departure_date = self.departure_date

        if not employee.user_id.partner_id:
            return

        for activity_type in self.plan_id.plan_activity_type_ids:
            self.env['mail.activity'].create({
                'res_id': employee.user_id.partner_id.id,
                'res_model_id': self.env['ir.model']._get('res.partner').id,
                'activity_type_id': activity_type.activity_type_id.id,
                'summary': activity_type.summary,
                'user_id': activity_type.get_responsible_id(employee).id,
            })
