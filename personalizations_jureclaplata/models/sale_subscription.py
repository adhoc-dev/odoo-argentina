from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    student_id = fields.Many2one('res.partner', string='Alumno', domain="[('parent_id', '=', partner_id), ('partner_type', '=', 'student')]")
    curso_actual = fields.Many2one(comodel_name='academic.group', string='Curso Actual',
                                   compute="_compute_curso_actual", store=True)

    @api.depends('student_id')
    def _compute_curso_actual(self):
        for rec in self:
            if (not rec.student_id):
                rec.curso_actual = False
            else:
                rec.curso_actual = rec.student_id.curso_actual

    @api.constrains('student_id')
    def _check_student(self):
        for rec in self:
            if rec.student_id and (not rec.student_id.partner_type or rec.student_id.partner_type != 'student'):
                raise UserError('Se está intentando asignar a un estudiante un contacto de otro tipo')

