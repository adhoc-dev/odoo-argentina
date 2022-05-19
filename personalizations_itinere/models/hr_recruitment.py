from odoo import models, fields

class Applicant(models.Model):
    _inherit = 'hr.applicant'

    born_date = fields.Date()
    address = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", domain="[('country_id.code', '=', 'AR')]")

    def create_employee_from_applicant(self):
        res = super().create_employee_from_applicant()
        for applicant in self:
            self.env['hr.employee'].browse(res['res_id']).write({
                'birthday': applicant.born_date
            })
            self.env['res.partner'].browse(self.env['hr.employee'].browse(res['res_id']).address_home_id.id).write({
                'street': applicant.address,
                'city': applicant.city,
                'state_id': applicant.state_id.id
            })
        return res
